
**General Overview:**
* The program uses the functionality of mongoDB in python (through pymongo) to build a system for creating document stores and then operating on them.
* The program consists of two main parts : Phase1 - Reading data files and creating collections in the database and Phase 2 - Performing search and update actions on the database built in Phase 1
* The system’s initial page contains a login screen where users can choose to provide a userID. If they do : a brief user report is displayed. Regardless of whether a user ID was provided, users can then perform certain actions and tasks.
* After performing an action, the user is brought back to the main menu and has the opportunity to go back to the screen where they can provide a new user ID or exit the program all together.
* The json files that contain the mongoDB collections are too big to upload to github. The typical format for a collection is -:\
      {\
        "Id": "1",\
        "PostTypeId": "1",\
        "AcceptedAnswerId": "23",\
        "CreationDate": "2010-08-10T18:54:58.893",\
        "Score": 30,\
        "ViewCount": 22710,\
        "Body": "<p>I am upgrading the internal SATA hard drive on my laptop from a 40G drive to a 160G            drive. ",\
        "OwnerUserId": "4",\
        "LastEditorUserId": "688",\
        "LastEditDate": "2011-07-24T19:42:06.517",\
        "LastActivityDate": "2016-08-16T10:36:44.840",\
        "Title": "How can I use DD to migrate data from an old drive to a new drive?",\
        "Tags": "<linux><freebsd><partition><storage><cloning>",\
        "AnswerCount": 7,\
        "CommentCount": 2,\
        "FavoriteCount": 11,\
        "ContentLicense": "CC BY-SA 3.0"\
      }

**User Guide:**
1. How do I connect to the mongoDB server?
(i) At the beginning of the programs, the user is prompted to enter the port number of the server they wish to connect to. This server should already be running in the background.

2. How do I build the database?
(i) Run the program “Phase1.py”. Have the files Posts.json, Votes.json, Tags.json in the same directory as Phase1.py.

Next,  run "Phase2.py"

3. How do I view a user report?
(i)When asked if you wish to provide a user Id, type “y”. A report will be displayed for the user Id entered.

4. How do I post a new question?
(i) When prompted to choose a task, type “1”

5. How do I search for questions by providing keywords?
(i)When prompted to choose a task, type “2”

6. How do I answer the selected question?
(i)After doing step 5, type “1” when prompted to choose an action

7. How do I view all answers to the selected question and select an answer?
(i)After doing step 5, choose “2” when prompted to choose an action

8. How do I vote on the selected question?
(i)After doing step 5, choose “3” when prompted to choose an action.

9. How do I vote on the selected answer from part 7?
(i)After doing step 7, the user will be asked whether they want to vote on the answer, type “y”.

10. How do I work with a new user ID?
After each task, the user will be asked whether they want to provide a new user ID, type “y”.

11. How do I exit the program?
After each task, the user will be asked whether they want to exit, type “y”.

**Flow of the program:**
Users first decide if they want to provide a user Id for which a report is displayed.
Then they can choose between Task #1 and #2. If Task #2 is chosen : they can perform 3 further actions.
After each action/task they are taken back to the main menu. At this point users may exit the program or
choose a new user id to work with.
