#Load on Beamlink One devices
#Serves captive portal for disaster relief victims, rescuers, and volunteers
from flask import Flask, render_template, request
import os
import json
import tweepy

app = Flask(__name__)

#beamlink_secretkey = os.environ.get('beamlink_secretkey')
#if beamlink_secretkey is None:
#	raise Exception('Beamlink secret key required')

cached_tweets = "" #Store the latest tweets in memory locally

#Test method
@app.route('/hello')
def hello_world():
    return 'Hello, World!'

#Main page
@app.route('/')
def index():
	return render_template('beamlink_captiveportal.html', tweets=tweets)
	#return render_template('index.html', tweets=cached_tweets)

#Receiver from the web server on the VPN host
@app.route('/refreshcache', methods=['POST'])
def refreshcache():
	secret_key = request.form.get("secret_key")
	if secret_key is None or secret_key != beamlink_secretkey:
		abort(401) #unauthorized access
	else:
		#Successful authentication
		tweets = request.form.get("tweets")
		if tweets is not None:
			#Tweets loaded
			cached_tweets = json.loads(tweets) #update cache
		else:
			print("No tweets sent in request")
			abort(412) #Error precondition failed (return to vpn)

