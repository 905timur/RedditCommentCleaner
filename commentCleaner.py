import praw
import time
import random
from datetime import datetime, timedelta, timezone

def get_reddit_credentials(credentials_file="credentials.txt"):
    """
    Retrieve Reddit client credentials from a file.

    Args:
        credentials_file (str): Path to the file containing Reddit client credentials.

    Returns:
        tuple: A tuple containing client_id, client_secret, username, and password.

    Notes:
        If the file does not exist, an error message is displayed, and the script exits.
    """
    try:
        with open(credentials_file, 'r') as f:
            client_id = f.readline().strip()
            client_secret = f.readline().strip()
            username = f.readline().strip()
            password = f.readline().strip()
        return client_id, client_secret, username, password
    except FileNotFoundError:
        print(
            "Error: Could not find the 'credentials.txt' file.\n"
            "Please create a 'credentials.txt' file in the same directory as the script with the following format:\n\n"
            "Your app ID\n"
            "Your secret\n"
            "Your username\n"
            "Your password"
        )
        exit()

def initialize_reddit(client_id, client_secret, username, password):
    """
    Initialize the Reddit instance with user credentials.

    Args:
        client_id (str): Reddit client ID.
        client_secret (str): Reddit client secret.
        username (str): Reddit username.
        password (str): Reddit password.

    Returns:
        praw.Reddit: An authenticated Reddit instance.
    """
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent='commentCleaner',
            validate_on_submit=True
        )
        reddit.user.me()
        print("Authenticated successfully.")
        return reddit
    except praw.exceptions.APIException as e:
        print("Error: Could not authenticate with the provided credentials.")
        exit()

def delete_old_comments(reddit, username, days_old, comments_deleted):
    """
    Delete comments older than a specified number of days.

    Args:
        reddit (praw.Reddit): Authenticated Reddit instance.
        username (str): Reddit username.
        days_old (int): Age limit for comments (in days).
        comments_deleted (list): A list to store deleted comments.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_old)
    for comment in reddit.redditor(username).comments.new(limit=None):
        comment_time = datetime.fromtimestamp(comment.created_utc, timezone.utc)
        if comment_time < cutoff_time:
            comment_date = comment_time.strftime("%Y-%m-%d %H:%M:%S")
            with open('deleted_comments.txt', 'a') as f:
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error deleting comment: {e}")

            # Add a random delay of 6-8 seconds between API calls
            time.sleep(random.uniform(6, 8))

def remove_comments_with_negative_karma(reddit, username, comments_deleted):
    """
    Remove comments with negative karma.

    Args:
        reddit (praw.Reddit): Authenticated Reddit instance.
        username (str): Reddit username.
        comments_deleted (list): A list to store deleted comments.
    """
    for comment in reddit.redditor(username).comments.new(limit=None):
        if comment.score <= 0:
            comment_time = datetime.fromtimestamp(comment.created_utc, timezone.utc)
            comment_date = comment_time.strftime("%Y-%m-%d %H:%M:%S")
            with open('deleted_comments.txt', 'a') as f:
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error removing comment: {e}")

            # Add a random delay of 6-8 seconds between API calls
            time.sleep(random.uniform(6, 8))

def remove_comments_with_one_karma_and_no_replies(reddit, username, comments_deleted):
    """
    Remove comments with one karma, no replies, and are at least a week old.

    Args:
        reddit (praw.Reddit): Authenticated Reddit instance.
        username (str): Reddit username.
        comments_deleted (list): A list to store deleted comments.
    """
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    for comment in reddit.redditor(username).comments.new(limit=None):
        comment_time = datetime.fromtimestamp(comment.created_utc, timezone.utc)
        if comment.score <= 1 and len(comment.replies) == 0 and comment_time < one_week_ago:
            comment_date = comment_time.strftime("%Y-%m-%d %H:%M:%S")
            with open('deleted_comments.txt', 'a') as f:
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error removing comment: {e}")

            # Add a random delay of 6-8 seconds between API calls
            time.sleep(random.uniform(6, 8))

def main():
    client_id, client_secret, username, password = get_reddit_credentials()
    reddit = initialize_reddit(client_id, client_secret, username, password)

    comments_deleted = []

    while True:
        action = input("Choose an action (1 - Delete old comments, 2 - Remove comments with negative karma, 3 - Remove comments with 1 karma and no replies, 4 - Quit): ")

        if action == '1':
            days_old = int(input("Enter the age limit for comments (in days): "))
            delete_old_comments(reddit, username, days_old, comments_deleted)
        elif action == '2':
            remove_comments_with_negative_karma(reddit, username, comments_deleted)
        elif action == '3':
            remove_comments_with_one_karma_and_no_replies(reddit, username, comments_deleted)
        elif action == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

        if comments_deleted:
            print(f"The script successfully deleted {len(comments_deleted)} comments.")
            comments_deleted = []

if __name__ == "__main__":
    main()
