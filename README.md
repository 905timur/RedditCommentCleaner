# Reddit Comment Cleaner v0.4
This Python script edits any Reddit comments older than 4 days to "." and then deletes them. 

To run this script:

-SYSTEM CONFIGURATION-

1. Install Python 3. 

2. Install praw by running the following code in terminal:

```
pip install praw
```


-REDDIT CONFIGURATION-

1. Navigate to https://www.reddit.com/prefs/apps

2. Click "Create application" at the bottom of the page

3. Select "script"

4. Fill out the discription, and both URL fields (you can point both fields to this README)

5. Click 'create app'

![image](https://user-images.githubusercontent.com/130249301/234336730-dbe61b3f-ffed-4f1f-ab35-b5fe1239d72c.png)


-SCRIPT CONFIGURATION-

Once your app is created, you will see your client ID, and secret. Both are highlighted below:

![image](https://user-images.githubusercontent.com/130249301/234361938-e09c0f87-e6b8-4b6b-9916-593b4bbcf35d.png)

1. Replace XXX with your client ID, secret, reddit username and passowrd into the following part of the script:

```
client_id = 'XXX'
client_secret = 'XXX'
username = 'XXX'
password = 'XXX'
```

2. (OPTIONAL) If you would like the script to delete comments either older or younger than 4 days, replace 4 with however many days you want in the following line of code:

```
if time.time() - comment.created_utc > 4 * 24 * 60 * 60:
```


-RUNNING THE SCRIPT-

1. Hit the Windows key on your keyboard and type 'cmd' into the search bar

2. Hit "Enter"

3. Navigate to wherever you saved the redditCleaner.py by using the "cd" command, for example:

```
cd C:\redditCleaner
```

4. Once in the same directory as redditCleaner.py, run the following command:

```
python redditCleaner.py```
