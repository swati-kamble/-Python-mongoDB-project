#mini project 2

import timeit

import json
from pymongo import MongoClient
import string

portNum = input("Enter the port number: ") 
client = MongoClient('mongodb://localhost:{}'.format(portNum)) 

#checking if database already exists
dblist = client.list_database_names()
if '291db' in dblist:
    client.drop_database('291db')
db = client['291db']
#checking if collections already exist
collist = db.list_collection_names()
if 'votes' in collist:
    db['votes'].drop()
if 'posts' in collist:
    db['posts'].drop()
if 'tags' in collist:
    db['tags'].drop()
#creating collections
votes = db["votes"]
posts = db["posts"]
tags = db["tags"]
#reading post file
with open('Posts.json','r') as data_file:    
    obj = json.load(data_file)
    data = obj['posts']['row']
#extracting terms
for post in data:
    terms = []
    if 'Title' in list(post.keys()):
        title = post['Title']+' '
        x = 0
        for i in range(0,len(title)):
            if title[i] in (string.punctuation + ' '):
                if len(title[x:i]) > 2 and (title[x:i].lower() not in terms):
                    terms.append(title[x:i].lower())
                x = i + 1
        
    if 'Body' in list(post.keys()):
        body = post['Body']+' '
        x = 0
        for i in range(0,len(body)):
            if body[i] in (string.punctuation + ' '):
                if len(body[x:i]) > 2 and (body[x:i].lower() not in terms):
                    terms.append(body[x:i].lower())
                x = i + 1
        
    if terms:
        post['Terms'] = terms

posts.insert_many(data)    
posts.create_index("Terms")

with open('Votes.json','r') as data_file:    
    obj = json.load(data_file)
    data = obj['votes']['row']
votes.insert_many(data)

with open('Tags.json','r') as data_file:    
    obj = json.load(data_file)
    data = obj['tags']['row']
tags.insert_many(data)

