# Connect to the default port on localhost for the mongodb server.
import pymongo
from datetime import date
from pymongo import MongoClient
from pprint import pprint
import timeit
import json
import string
import re
db = None
votes = None
posts = None
tags = None

def pidcount():

    pcount = posts.count_documents({})
    return pcount
def newpid(pcount):
    #while posts.find_one({"Id":str(pcount)}):
    #while posts.count_documents({"Id":str(pcount)})>0: #pid RECURSION
    pid = "p"+str(pcount)
    check = posts.find_one({"Id": pid})
    if check:
        pcount+=1
        pid = newpid(pcount)
        return pid
    return pid
def vidcount():
    vcount = votes.count_documents({})
    return vcount
def newvid(vcount):
    vid = "v"+str(vcount)
    check = votes.find_one({"Id":str(vid)})
    if check:
        vcount+=1
        vid=newvid(vcount)
        return vid
    return vid
def tidcount():
    tcount = tags.count_documents({})
    return tcount
def newtid(tcount):
    tid = "t"+str(tcount)
    check = tags.find_one({"Id":str(tcount)})
    if check:
        tcount+=1
        tid=newtid(tcount)
        return tid
    return tid
#question 1
def question():
    pcount = pidcount()
    Id = newpid(pcount)
    q_title = input("Enter a question title: ")
    q_body = input("Enter the question body: ")
    tags_entered = input("Enter tags followed by space: ")
    tag_list = []
    tag_list = list(tags_entered.split(" "))
    insertags =[]
    for tag in tag_list: 
        results = tags.find_one({"TagName":tag})
        if not results: #we have to check if tags are in tags document
            tcount = tidcount()
            tid = newtid(tcount)
            insert = [
                {
                    "Id":str(tid),
                    "TagName":tag,
                    "Count":'1'
                }
            ]
            insertags.append(tag)
            tags.insert_many(insert)
            print("Tag Inserted")
        else: #increasing tag count
            count = int(results["Count"])
            print(" tag count:",count,"--> ",count+1)
            count+=1
            tags.update_one(
            {"TagName":tag},
            {"$set":{"Count":str(count)}}
            )
            if tag not in insertags:
                insertags.append(tag)
            
    today = str(date.today())
    if uid:
        post = [
            {
                "Id":str(Id),"PostTypeId": "1","CreationDate": today,"Score": "0",
                "ViewCount": "0","Title": q_title,"Body":q_body,"Tags":tags_entered,
                "OwnerUserId": uid,
                "AnswerCount": "0",
                "CommentCount": "0",
                "FavoriteCount": "0",
                "ContentLicense": "CC BY-SA 2.5"}
        ]
    else:
        post = [
            {
                "Id":str(Id),"PostTypeId": "1","CreationDate": today,"Score": "0",
                "ViewCount": "0","Title": q_title,"Body":q_body,"Tags":tags_entered,
                "AnswerCount": "0",
                "CommentCount": "0",
                "FavoriteCount": "0",
                "ContentLicense": "CC BY-SA 2.5"}
        ]



    posts.insert_many(post)
#question 2
def qsearch():

    while True:
        try: 
            n=int(input("How many Keywords would you like to enter? "))
            if n<1:
                print("Please enter a number greater than 0.")
                continue
            break
        except:
            pass
        print("Please enter an integer within the range.")

    keywords = [] #contains all keywords
    match = [] #contains all documents that have the keyword
    while n!=0:
        keywords.append(input("Enter Keyword: "))
        n = n-1
        
    for key in keywords:
        if len(key)>2:
            results = posts.find({"PostTypeId": "1","$or":[{"Terms":key},{"Tags":key}]})
            rcount = posts.count_documents({"PostTypeId": "1","$or":[{"Terms":key},{"Tags":key}]})
        else:
            results = posts.find({"PostTypeId": "1","$or":[{"Body":{"$regex": key,"$options" :'i'}},{"Title":{"$regex": key,"$options" :'i'}},{"Tags":{"$regex": key,"$options" :'i'}}]})
            rcount = posts.count_documents({"PostTypeId": "1","$or":[{"Body":{"$regex": key,"$options" :'i'}},{"Title":{"$regex": key,"$options" :'i'}},{"Tags":{"$regex": key,"$options" :'i'}}]})
        if rcount>0: #if there are matches
            for document in results:
                #print(document)
                match.append(document) 
    if len(match) > 0:
        i=1
        for row in match: #prints out specific columns
            #print(i,'--','Title:',row["Title"],' |Creation Date:',row["CreationDate"],' |Score:',row["Score"],' |Answer Count:',row["AnswerCount"])
            try:
                print(i,'--','Title:',row["Title"],' |Creation Date:',row["CreationDate"],' |Score:',row["Score"],' |Answer Count:',row["AnswerCount"])
                i+=1
            except:
                pass
    else:
        print("no matches found")
        return

    #post choice
    if match:
        while True:
            try:
                while True:
                    choice = int(input("Select Post No. (1/2/3...): "))
                    if choice > len(match) or choice < 1:
                        print("Selected post not in range.")
                        continue
                    break
                break
            except:
                pass
            print("please enter an integer")
        pick = match[choice-1]
    
    #displaying all rows of question
    pprint(pick)
    #increasing view count
    if "ViewCount" in list(pick.keys()):
        viewcnt = int(pick["ViewCount"])
        print("viewcnt:",viewcnt,"--> ",viewcnt+1)
        viewcnt+=1
        posts.update_one(
            {"Id":pick["Id"]},
            {"$set":{"ViewCount":str(viewcnt)}}
        )
        return pick
#question 3
def answer(pick):
    # check if post type id is 1 to check if its a question
    parent = pick["Id"]
    #print("pick id:",parent)
    #results = posts.find({'$and':[{"PostTypeId": "1"},{"Id":parent}]})
    rcount = posts.count_documents({'$and':[{"PostTypeId": "1"},{"Id":parent}]})
    if rcount >0:
        #get a unique pid

        pcount = pidcount()
        pid = newpid(pcount)
        
        #prompting user to input answer
        a_body = input("Enter the answer ")        
        today = str(date.today())    
        if uid:
            post = [{'Id': pid, 
                    'PostTypeId': "2", 
                    'ParentId': parent, 
                    'CreationDate': today, 
                    'Score': "0", 
                    'Body': a_body,
                    'OwnerUserId': uid,
                    'CommentCount': "0", 
                    'ContentLicense': 'CC BY-SA 2.5'}]
        else: # checks uid
            post = [{'Id': pid, 
                    'PostTypeId': "2", 
                    'ParentId': parent, 
                    'CreationDate': today, 
                    'Score': "0", 
                    'Body': a_body,
                    'CommentCount': "0", 
                    'ContentLicense': 'CC BY-SA 2.5'}]  
        #insert into posts collection       
        posts.insert_many(post)
        print("Answer updated")
    else:
        print("The selected post is an answer")
#question 4
def printans(pick):
    newList = []
    index = 1
    parent = pick['Id']
    new = posts.find_one({"$and": [{"PostTypeId": "1"}, {"Id": str(parent)}, {"AcceptedAnswerId":{'$exists': True}}]})
    aid = None
    if new:
        aid = new["AcceptedAnswerId"]
        new2 = posts.find_one({"$and": [{"PostTypeId": "2"}, {"Id": str(aid)}]})
        print(index, "[ * "+'%.80s'%str(new2["Body"]), str(new2["CreationDate"]), str(new2["Score"])+"]")
        newList.append(new2)
        results = posts.find({"$and": [{"PostTypeId": "2"}, {"ParentId": str(parent)}, {'Id': {'$ne': str(aid)}}]})
        index = index + 1
        for i in results:
            newList.append(i)

        for x in range(1,len(newList)):
            print(index, "[ "+'%.80s'%str(newList[x]["Body"]), str(newList[x]["CreationDate"]), str(newList[x]["Score"])+"]")
            index = index + 1
    else:
        results = posts.find({"$and": [{"PostTypeId": "2"}, {"ParentId": str(parent)}]})
        COUNT = posts.count_documents({"$and": [{"PostTypeId": "2"}, {"ParentId": str(parent)}]})
        if COUNT>0:
            for i in results:
                newList.append(i)

            for x in range(0,len(newList)):
                print(index, "[ "+'%.80s'%str(newList[x]["Body"]), str(newList[x]["CreationDate"]), str(newList[x]["Score"])+"]")
                index += 1
        else:
            print("No answers for selected question")
            return
    if newList:
        uchoice = input("Would you like to Select an Answer? (y/n): ")
        if uchoice.lower() == 'y':
            while(True):
                try:
                    #choice = input("Do you want to choose an answer?")
                # if choice == Y.lower()
                    selection = int(input("Select (1/2/3..etc):  "))
                    if selection>0 and selection<index:
                        break
                    else:
                        print("Please enter a valid number")
                except Exception:
                    print("Please enter a number")
                    continue
        else:
            return
    pickans = None
    pickans = newList[selection - 1]
    print(pickans)
    return pickans
#question 5
def vote(pick):
    vcount = vidcount()
    vcount+=1
    vid = newvid(vcount)
    pid = str((pick["Id"]))
    today = str(date.today())
    if uid:
    #check if user has voted on post
        ucount = votes.count_documents({"$and":[{"UserId": uid},{"PostId":pid}]})
        if ucount>0: #user has voted before
            print("You have already voted on this post")
            #exit to login screen

        else: #user has not voted before
            newdict = [{
            "Id": str(vid),
            "PostId": str(pid),
            "VoteTypeId": "2",
            "UserId":uid,
            "CreationDate": today
            }]
            votes.insert_many(newdict)
            #updating score
            if "Score" in list(pick.keys()):
                score = int(pick["Score"])
                print("score:",score,"--> ",score+1)
                score+=1
                posts.update_one(
                {"Id":pick["Id"]},
                {"$set":{"Score":str(score)}}
                )
        #----27017
    else: # not registered user
        newdict = [{
        "Id": str(vid),
        "PostId": str(pid),
        "VoteTypeId": "2",
        "CreationDate": today
        }]
        votes.insert_many(newdict)
        #updating score
        if "Score" in list(pick.keys()):
            score = int(pick["Score"])
            print("score:",score,"--> ",score+1)
            score+=1
            posts.update_one(
            {"Id":pick["Id"]},
            {"$set":{"Score":str(score)}}
            )
        
def interface():
    global uid
    uid = None
    while(True):
        printLine()
        print("WELCOME!")
        printLine() 
        uid = report()
        while(True):
            print("You can perform the following tasks: ")
            print("1. Post a question")
            print("2. Search for questions")
            choice = input("Select a task (1/2): ")
            printLine()
            if choice == '1':
                question()
            elif choice == '2':
                pick = []
                pick = qsearch()
                if not pick:
                    continue
                print("Having selected a question, you can perform these actions:")
                print("1. Answer the selected question.")
                print("2. View all answers of the selected question and select an answer.")
                print("3. Vote on selected post (answer/question).")
                choice2 = input("Select an action (1/2/3): ")
                if choice2 == '1':
                    answer(pick)
                elif choice2 == '2':
                    pickans = printans(pick) #catch the list of the selected ans
                    if pickans:
                        voteans = input("Would you like to Vote on this Answer? (y/n):")
                        if voteans.lower() == 'y':
                            vote(pickans)
                elif choice2 == '3':
                    vote(pick)
                else:
                    print("Not an appropriate input, redirecting to main menu ...")
            else:
                print("Not an appropriate input, redirecting to main menu ...")
            printLine()
            to_exit = input("Do you wish to exit? (y/n): ")
            if to_exit.lower() == 'y':
                print("Exiting...")
                exit(0)
            back_to_user = input("Do you wish to provide a new user ID?(y/n): ")
            if back_to_user.lower() == 'y':
                break
def printLine():
    print('-'* 70)
def report():
    generateReport = input("Do you wish to provide a user ID? y/n: ")
    if generateReport.lower() == 'y':
        printLine()
        uid = input("Enter user ID: ")
        print("REPORT FOR USER {}".format(uid))
        results = posts.aggregate([
            {"$match":{'$and':[{'OwnerUserId': '{}'.format(uid)}, {'PostTypeId':'1'}]}},
            {"$group":{"_id":"$OwnerUserId","numQs":{"$sum":1},"avgScore":{"$avg":"$Score"}}}
        ])
        is_empty = True
        
        for result in results:
            print("1. Number of questions owned:",result["numQs"])
            print("2. Average score of questions:",result["avgScore"])
            is_empty = False

        if is_empty:
            print("1. Number of questions owned: 0")
            print("2. Average score of questions: 0")

        results = posts.aggregate([
            {"$match":{'$and':[{'OwnerUserId': '{}'.format(uid)}, {'PostTypeId':'2'}]}},
            {"$group":{"_id":"$OwnerUserId","numAs":{"$sum":1},"avgScore":{"$avg":"$Score"}}}
        ])

        is_empty = True
        for result in results:
            print("3. Number of answers owned:",result["numAs"])
            print("4. Average score of answers:",result["avgScore"])
            is_empty = False
        
        if is_empty:
            print("3. Number of answers owned: 0")
            print("4. Average score of answers: 0")
        
        results = votes.aggregate([
        {"$match":{"UserId":'{}'.format(uid)}},
        {"$group":{"_id":"$UserId","numVo":{"$sum":1}}} 
        ])
        is_empty = True
        for result in results:
            print("5. Number of Votes registered:",result["numVo"])
            is_empty = False
        
        if is_empty:
            print("5. Number of Votes registered: 0") 

        return uid
    printLine()
    return
def main():
    global db,votes,posts,tags
    portNum = input("Enter the port number: ") 
    client = MongoClient('mongodb://localhost:{}'.format(portNum)) 
    #phase1()
    #client = MongoClient()
    db = client["291db"]
    votes = db["votes"]
    posts = db["posts"]
    tags = db["tags"]

     #counting pid
    
    colist = db.list_collection_names()
    if "posts" in colist:
        print("connection succesful") #checks if connection succesful
        
    interface()

    #check if matches is empty

    #question 5

        
main()