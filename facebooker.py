#!/usr/bin/python3.6

from twython import Twython
from elasticsearch import Elasticsearch
import requests
import json
import pprint

es = Elasticsearch()
pp = pprint.PrettyPrinter(indent=4)

with open("twitter_credentials.json", "r") as file:  
    creds = json.load(file)

python_tweets = Twython(creds["CONSUMER_KEY"], creds["CONSUMER_SECRET"])
#"geocode": "-28.0173,153.4257,200km",
query = {"q": "gold coast tennis",  
        "result_type": "mixed",
        "count": 100,
        "lang": "en",
        }

response = python_tweets.search(**query)

i=0

for line in response["statuses"]:

    keys = line.keys()

    obj = {}

    hashtags = []
    user_mentions = []

    text = ""
    followers_count = 0
    name = ""
    screen_name = ""

    if "entities" in keys:
        entity_keys = line["entities"].keys()
        if "hashtags" in entity_keys:
            hashtags = line["entities"]["hashtags"]
        if "user_mentions" in entity_keys:
            user_mentions = line["entities"]["user_mentions"]
    
    if "text" in keys:
        text = line["text"]

    if "user" in keys:
        user = line["user"]
        user_keys = user.keys()
        if "followers_count" in user_keys:
            followers_count = user["followers_count"]
        if "name" in user_keys:
            name = user["name"]
        if "screen_name" in user_keys:
            screen_name = user["screen_name"]

    if len(hashtags) > 0:
        obj["hashtags"] = []
        for hashtag in hashtags:
            obj["hashtags"].append(hashtag["text"])
    if len(user_mentions) > 0:
        obj["user_mentions"] = []
        for user_mention in user_mentions:
            obj["user_mentions"].append({"name": user_mention["name"], "screen_name": user_mention["screen_name"]})


    obj["name"] = name
    obj["screen_name"] = screen_name
    obj["followers"] = followers_count
    obj["text"] = text

    #es.index(index="twitter_tennis", doc_type="gold_coast_tennis", id=i, body=obj)

    #i+=1

a = es.search(index='twitter_tennis', doc_type='gold_coast_tennis')
print(a)