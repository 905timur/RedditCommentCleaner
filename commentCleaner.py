import praw
import time

client_id = input("Enter your Reddit client ID: ")
client_secret = input("Enter your Reddit client secret: ")
username = input("Enter your Reddit username: ")
password = input("Enter your Reddit password: ")

while True:
    days_old = input("Enter how old (in days) the comments should be: ")
    try:
        days_old = int(days_old)
        break
    except ValueError:
        print("Error: Please enter a number.")

confirmation = input("Do you want to run the script? (yes/no): ")
if confirmation.lower() != 'yes':
    print("Script aborted.")
    exit()

subreddit_name = 'your_subreddit_name'

try:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent='commentCleaner'
    )
    reddit.user.me() # Check if authentication succeeded
except Exception as e:
    print("Error: Could not authenticate with the provided credentials.")
    exit()

comments_deleted = []

def delete_old_comments():
    for comment in reddit.redditor(username).comments.new(limit=None):
        if time.time() - comment.created_utc > days_old * 24 * 60 * 60:
            comment.edit(".")
            comment.delete()
            comments_deleted.append(comment)

while True:
    print("Working...", end="\r")
    delete_old_comments()
    time.sleep(1)

    if len(comments_deleted) > 0:
        print("The script ran successfully and deleted {} comments.".format(len(comments_deleted)))
        comments_deleted = []
    else:
        print("There were no comments to delete.")
