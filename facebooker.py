#!/usr/bin/python3.6

from twython import Twython  
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

with open("twitter_credentials.json", "r") as file:  
    creds = json.load(file)

python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

query = {'q': 'tennis',
         'geocode': '-28.0173,153.4257,50km',
        'result_type': 'mixed',
        'count': 100,
        'lang': 'en',
        }
    
response = python_tweets.search(**query)

for line in response['statuses']:
    pp.pprint(line)