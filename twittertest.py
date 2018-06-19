from flask import Flask, render_template
import tweepy
import os
import json

app = Flask(__name__)
consumer_key = os.environ.get('twitter_consumerkey')
consumer_secret = os.environ.get('twitter_consumersecret')
access_token = os.environ.get('twitter.accesstokenkey')
access_token_secret = os.environ.get('twitter.accesstokensecret')

#Target server ip addresses
#Target port: 5000 for each server (important)
clients = ['10.8.0.6']

if consumer_key is None:
	raise Exception('Consumer key required')

if consumer_secret is None:
	raise Exception('Consumer secret required')

if access_token is None:
	raise Exception('Access token required')

if access_token_secret is None:
	raise Exception('Access token secret required')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth) #Initialize the API

results = api.search(q="fema", count=1) #Fill query with desired information
tweets = [] #Blank list, will be filled with tweets but with most data cut out
for result in results: #For each tweet
	raw_json = result._json
	#Pull all relevant information out of the tweets
	text = raw_json.get("text", "Error: No text")
	favorites = raw_json.get("favorite_count", 0)
	retweets = raw_json.get("retweet_count", 0)
	username = raw_json.get("user", "No name").get("name", "No name")
	date = raw_json.get("created_at")
	lang = raw_json.get("lang")
	tweetObj = {} #Define a new dictionary and populate key value pairs of relevant information
	tweetObj["text"] = text
	tweetObj["favorites"] = favorites
	tweetObj["retweets"] = retweets
	tweetObj["username"] = username
	tweetObj["date"] = date
	tweetObj["lang"] = lang
	tweets.append(tweetObj)

print(json.dumps(tweets))
