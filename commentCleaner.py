import praw
import time
from datetime import datetime, timedelta

def get_reddit_credentials(credentials_file="Credentials.txt"):
    """
    Prompt the user to input Reddit client credentials.

    Args:
        credentials_file (str): Path to the file containing Reddit client credentials.

    Returns:
        tuple: A tuple containing client_id, client_secret, username, and password.
    """
    try:
        with open(credentials_file, 'r') as f:
            client_id = f.readline().strip()
            client_secret = f.readline().strip()
            username = f.readline().strip()
            password = f.readline().strip()
            validate_on_submit=True
            return client_id, client_secret, username, password
    except FileNotFoundError:
        print("Error: Could not find the credentials file.")
    
    # If file reading fails or file is not found, prompt the user to input credentials manually
    client_id = input("Enter your Reddit client ID: ")
    client_secret = input("Enter your Reddit client secret: ")
    username = input("Enter your Reddit username: ")
    password = input("Enter your Reddit password: ")
    validate_on_submit=True

    return client_id, client_secret, username, password, validate_on_submit


def get_days_old():
    """
    Prompt the user to input the age limit for comments.

    Returns:
        int: The number of days for the age limit.
    """
    while True:
        days_old = input("Enter how old (in days) the comments should be: ")
        try:
            days_old = int(days_old)
            return days_old
        except ValueError:
            print("Error: Please enter a number.")

def confirm_and_run():
    """
    Ask the user for confirmation to run the script.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    confirmation = input("Do you want to run the script? (yes/no): ")
    return confirmation.lower() == 'yes' or confirmation.lower() == 'y'

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

    Notes:
        This function will delete comments older than the specified age limit.
    """
    for comment in reddit.redditor(username).comments.new(limit=None):
        if time.time() - comment.created_utc > days_old * 24 * 60 * 60:
            comment_date = datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S")
            with open('deleted_comments.txt', 'a') as f:
                # Write the date, karma score, and comment body to the file
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error deleting comment: {e}")


def remove_comments_with_negative_karma(reddit, username, comments_deleted):
    """
    Remove comments with negative karma.

    Args:
        reddit (praw.Reddit): Authenticated Reddit instance.
        username (str): Reddit username.
        comments_deleted (list): A list to store deleted comments.

    Notes:
        This function will remove comments with a negative karma score.
    """
    for comment in reddit.redditor(username).comments.new(limit=None):
        if comment.score <= 0:
            comment_date = datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S")
            with open('deleted_comments.txt', 'a') as f:
                # Write the date, karma score, and comment body to the file
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error removing comment: {e}")
                
                
def remove_comments_with_one_karma_and_no_replies(reddit, username, comments_deleted):
    """
    Remove comments with one karma, no replies, and are at least a week old.

    Args:
        reddit (praw.Reddit): Authenticated Reddit instance.
        username (str): Reddit username.
        comments_deleted (list): A list to store deleted comments.

    Notes:
        This function will remove comments with a karma score of 1, no replies, and are at least a week old.
        It will append the deleted comments with their creation date, karma score, and comment body to the 'deleted_comments.txt' file.
    """
    # Define a timedelta of one week
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    for comment in reddit.redditor(username).comments.new(limit=None):
        # Check if the comment meets the criteria
        if comment.score <= 1 and len(comment.replies) == 0 and datetime.utcfromtimestamp(comment.created_utc) < one_week_ago:
            # Format the date of the comment
            comment_date = datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S")

            with open('deleted_comments.txt', 'a') as f:
                # Write the date, karma score, and comment to the file
                f.write(f"{comment_date} | {comment.score} | {comment.body}\n")
            try:
                comment.edit(".")
                comment.delete()
                comments_deleted.append(comment)
            except praw.exceptions.APIException as e:
                print(f"Error removing comment: {e}")

def main():
    client_id, client_secret, username, password = get_reddit_credentials()

    if not confirm_and_run():
        print("Script aborted.")
        return

    reddit = initialize_reddit(client_id, client_secret, username, password)

    comments_deleted = []

    while True:
        action = input("Choose an action (1 - Delete old comments, 2 - Remove comments with negative karma, 3 - Remove comments with 1 karma and no replies, 4 - Quit): ")

        if action == '1':
            print("Working (Deleting old comments)...", end="\r")
            days_old = get_days_old()
            delete_old_comments(reddit, username, days_old, comments_deleted)
        elif action == '2':
            print("Working (Removing comments with negative karma)...", end="\r")
            remove_comments_with_negative_karma(reddit, username, comments_deleted)
        elif action == '3':
            print("Working (Removing comments with one karma and no replies)...", end="\r")
            remove_comments_with_one_karma_and_no_replies(reddit, username, comments_deleted)
        elif action == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

        time.sleep(1)

        if len(comments_deleted) > 0:
            print("The script ran successfully and deleted {} comments.".format(len(comments_deleted)))
            comments_deleted = []
        else:
            print("There were no comments to delete.")

if __name__ == "__main__":
    main()
