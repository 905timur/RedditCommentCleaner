# Reddit Comment Cleaner v1.9

This Python script edits any Reddit comments older than a specified number of days to "." and then deletes them. It also provides options to delete comments with negative karma or those with specific criteria.

---

## **SYSTEM CONFIGURATION**

1. Install Python 3.

2. Install `praw` by running the following command in your terminal:

    ```bash
    pip install praw
    ```

---

## **REDDIT CONFIGURATION**

1. Navigate to [Reddit Apps Preferences](https://www.reddit.com/prefs/apps).

2. Click "Create application" at the bottom of the page.

3. Select "script".

4. Fill out the description, and both the URL and redirect URI fields (you can point both fields to this GitHub page).

5. Click "create app".

    ![image](https://user-images.githubusercontent.com/130249301/234336730-dbe61b3f-ffed-4f1f-ab35-b5fe1239d72c.png)

6. Once your app is created, you will see your client ID and client secret. Both are highlighted below:

    ![image](https://user-images.githubusercontent.com/130249301/234361938-e09c0f87-e6b8-4b6b-9916-593b4bbcf35d.png)

---

## **SCRIPT CONFIGURATION**

1. Create a file named `credentials.txt` in the same directory as the script. This file should contain your Reddit API credentials in the following format:

    ```
    Your app ID
    Your secret
    Your username
    Your password
    ```

2. Save the file.

---

## **RUNNING THE SCRIPT**

1. Clone this repository using the following command in your terminal:

    ```bash
    git clone https://github.com/905timur/RedditCommentCleaner.git
    ```

2. Navigate to the directory where you cloned the repository:

    ```bash
    cd RedditCommentCleaner
    ```

3. Run the script using the following command:

    ```bash
    python commentCleaner.py
    ```

4. You will be prompted to choose one of the following options:

    ```
    Run options
    1. Remove all comments older than x days
    2. Remove comments with negative karma
    3. Remove comments with 1 karma and no replies
    4. Quit
    ```

5. Follow the instructions for the selected option. Deleted comments will be logged in a file named `deleted_comments.txt` in the same directory as the script.

---

## **NOTES**

- Ensure the `credentials.txt` file exists and follows the specified format. The script will exit if this file is not found.
- Deleted comments are saved in `deleted_comments.txt`, including their timestamp, score, and original text.

---

## **CHANGELOG**

### v1.9
- Removed credential prompts from the script; credentials are now loaded from a `credentials.txt` file.
- Replaced deprecated `datetime` methods with timezone-aware implementations for improved reliability.

For further suggestions or questions, please contact me or open an issue on this repository.
