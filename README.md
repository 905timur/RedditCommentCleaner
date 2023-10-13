# Reddit Comment Cleaner v1.5

This Python script edits any Reddit comments older than x amount of days to "." and then deletes them.

**<u>PLEASE USE ONLY commentCleaner.py, commentCleaner-v0.4 has to be manually configured and I do not recommend using it.**</u>

**-SYSTEM CONFIGURATION-**

1. Install Python 3. 

2. Install praw by running the following code in terminal:

```
pip install praw
```


**-REDDIT CONFIGURATION-**

1. Navigate to https://www.reddit.com/prefs/apps

2. Click "Create application" at the bottom of the page

3. Select "script"

4. Fill out the discription, and both URL and URI fields (you can point both fields to this Github page)

5. Click 'create app'

![image](https://user-images.githubusercontent.com/130249301/234336730-dbe61b3f-ffed-4f1f-ab35-b5fe1239d72c.png)


**-SCRIPT CONFIGURATION-**

Once your app is created, you will see your client ID, and secret. Both are highlighted below:

![image](https://user-images.githubusercontent.com/130249301/234361938-e09c0f87-e6b8-4b6b-9916-593b4bbcf35d.png)

1. When the script is executed, you will be prompted to enter your Client ID, secret, username and password.

2. The last prompt will ask you how old the comments should be that are being deleted. For example, if you enter "4", all comments older than 4 days old will be deleted.




-RUNNING THE SCRIPT-

1. Copy commentCleaner.py code into notepad and save it in whatevery directory you prefer as commentCleaner.py, alternatively you can copy the repository using the following command in Windows terminal:

```
git clone https://github.com/905timur/RedditCommentCleaner.git
```

2. In Windows terminal, navigate to wherever you saved the commentCleaner.py by using the "cd" command, for example:

```
cd C:\commentCleaner
```

3. Once in the same directory as commentCleaner.py, run the following command:

```
python commentCleaner.py
```

4. Fill out all the prompts. 
