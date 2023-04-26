import praw
import time

client_id = 'XXX'
client_secret = 'XXX'
username = 'XXX'
password = 'XXX'


try:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent='commentCleaner'
    )
except Exception as e:
    print(f"Error: Could not authenticate with the provided credentials. {str(e)}")
    exit()

comments_deleted = []

def delete_old_comments():
    for comment in reddit.redditor(username).comments.new(limit=None):
        if time.time() - comment.created_utc > 4 * 24 * 60 * 60:
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
