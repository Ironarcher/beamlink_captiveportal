import tweepy
import os
import json
import requests
import time
consumer_key = os.environ.get('twitter_consumerkey')
consumer_secret = os.environ.get('twitter_consumersecret')
access_token = os.environ.get('twitter.accesstokenkey')
access_token_secret = os.environ.get('twitter.accesstokensecret')
beamlink_secretkey = os.environ.get('beamlink_secretkey')

#Target server ip addresses
#Target port: 5000 for each server (important)
clients = ['10.8.0.6']
port = 5000
delay_time = 60 #Time between updates sent (in seconds)

if consumer_key is None:
	raise Exception('Consumer key required')

if consumer_secret is None:
	raise Exception('Consumer secret required')

if access_token is None:
	raise Exception('Access token required')

if access_token_secret is None:
	raise Exception('Access token secret required')

#This secret key is to prevent unauthorised access to the interface on the beamlink One devices
#The other security measure is to prevent access from the outside on port 5000
if beamlink_secretkey is None:
	raise Exception('Beamlink secret key required')

#Returns the API object for tweepy
#Use to refresh access
def init_twitter():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	return tweepy.API(auth)

def updateCache():
	api = init_twitter()
	results = api.search(q="fema", count=2) #Fill query with desired information
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
	postPackage = json.dumps(tweets) #Convert data object into a string
	sendNewData(postPackage) #Send to clients

#Send a POST request to each webserver address listed under the clients list with the updated tweets/information
def sendNewData(tweets):
	for client in clients: #For each beamlink system to update
		target = "http://" + client + ":" + str(port)
		try:
			payload = {"secret_key" : beamlink_secretkey, "tweets" : tweets} #Generate the payload for POST request
			r = requests.post(target, data=payload)
			if r.status_code != requests.code.ok: #If the status code is not acceptable, report the error to the console
				print "Error occured when posting to: " + client
				print r.status_code
		except Exception, e:
			print e.message

if __name__ == "__main__":
	while(True):
		updateCache()
		sleep(delay_time)
