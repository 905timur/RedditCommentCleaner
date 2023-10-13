import praw
import time


def get_reddit_credentials():
    client_id = input("Enter your Reddit client ID: ")
    client_secret = input("Enter your Reddit client secret: ")
    username = input("Enter your Reddit username: ")
    password = input("Enter your Reddit password: ")
    return client_id, client_secret, username, password

def get_days_old():
    while True:
        days_old = input("Enter how old (in days) the comments should be: ")
        try:
            days_old = int(days_old)
            return days_old
        except ValueError:
            print("Error: Please enter a number.")

def confirm_and_run():
    confirmation = input("Do you want to run the script? (yes/no): ")
    return confirmation.lower() == 'yes' or confirmation.lower() == 'y'

def initialize_reddit(client_id, client_secret, username, password):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent='commentCleaner',
            validate_on_submit=True  # Handle the DeprecationWarning
        )
        reddit.user.me()  # Check if authentication succeeded
        return reddit
    except Exception as e:
        print("Error: Could not authenticate with the provided credentials.")
        exit()

def delete_old_comments(reddit, username, days_old, comments_deleted):
    for comment in reddit.redditor(username).comments.new(limit=None):
        if time.time() - comment.created_utc > days_old * 24 * 60 * 60:
            with open('deleted_comments.txt', 'a') as f:
                f.write(comment.body + '\n')
            comment.edit(".")
            comment.delete()
            comments_deleted.append(comment)

def remove_comments_with_negative_karma(reddit, username, comments_deleted):
    for comment in reddit.redditor(username).comments.new(limit=None):
        if comment.score < 0:
            with open('deleted_comments.txt', 'a') as f:
                f.write(comment.body + '\n')
            comment.edit(".")
            comment.delete()
            comments_deleted.append(comment)

def main():

    client_id, client_secret, username, password = get_reddit_credentials()

    if not confirm_and_run():
        print("Script aborted.")
        return

    reddit = initialize_reddit(client_id, client_secret, username, password)

    comments_deleted = []

    while True:
        action = input("Choose an action (1 - Delete old comments, 2 - Remove comments with negative karma, 3 - Quit): ")

        if action == '1':
            print("Working (Deleting old comments)...", end="\r")
            days_old = get_days_old()
            delete_old_comments(reddit, username, days_old, comments_deleted)
        elif action == '2':
            print("Working (Removing comments with negative karma)...", end="\r")
            remove_comments_with_negative_karma(reddit, username, comments_deleted)
        elif action == '3':
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
