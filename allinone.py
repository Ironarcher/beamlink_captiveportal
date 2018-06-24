#Load on Beamlink One devices
#Serves captive portal for disaster relief victims, rescuers, and volunteers
from flask import Flask, render_template, request
import os
import json
import tweepy
import time

app = Flask(__name__)
consumer_key = os.environ.get('twitter_consumerkey')
consumer_secret = os.environ.get('twitter_consumersecret')
access_token = os.environ.get('twitter_accesstokenkey')
access_token_secret = os.environ.get('twitter_accesstokensecret')

#verify all keys are pulled from the system
if consumer_key is None:
	raise Exception('Consumer key required')

if consumer_secret is None:
	raise Exception('Consumer secret required')

if access_token is None:
	raise Exception('Access token required')

if access_token_secret is None:
	raise Exception('Access token secret required')

cached_tweets = [] #Store the latest tweet id's locally to prevent refreshing every time user requests tweet ID's and using up all of the API calls
last_updated = time.time() #Set time (in seconds) when the program loaded
refresh_time = 10 #Minimum time in seconds before cache expires

#Returns the API object for tweepy
#Use to refresh access
def init_twitter():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	return tweepy.API(auth)

def searchTweets():
	api = init_twitter()
	results = api.search(q="fema", count=5) #Fill query with desired information
	urls = [] #Blank list, will be filled with tweets but with most data cut out
	for result in results: #For each tweet
		#print result.entities.get('urls')[0].get('expanded_url')
		tweetid = result.id
		username = result._json.get("user").get("screen_name")
		print tweetid
		print username
		urls.append("https://www.twitter.com/" + username + "/status/" + str(tweetid))
	print urls
	cached_tweets = urls #Update cache with new information
	return urls

#Main page
@app.route('/')
def index():
	print cached_tweets
	if time.time() - last_updated >= refresh_time or len(cached_tweets) == 0: #If the cache has expired, or the cache is empty and there is no tweets to display
		tweet_urls = searchTweets() #Use updated information
	else:
		tweet_urls = cached_tweets #Else use cached information
	return render_template('beamlink_captiveportal.html', tweets=tweet_urls) #Render template, with list of tweet id's to display using twitter's lightweight javascript library

