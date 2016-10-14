#!/usr/bin/python3
# redditParse.py - returns the home page of given subreddit then saves the JSON data
# Usage:
# redditParse.py <subreddit> <filename> -	pass a subreddit and a filename
#											to save the JSON
# redditParse.py <subreddit> -	pass only a subreddit and it will be saved
#								as the subreddit w/ timestamp JSON
# redditParse.py -	pass nothing and it will grab the front page and save w/
#					timestamp

import sys, json, requests, pprint, time, datetime

USER_AGENT = {'user-agent': 'Linux:redditParse.py test script v0.0.2'}
URL_BASE = 'https://www.reddit.com/'

# Download the JSON data from reddit.com's API
# If given a subreddit get that else front page
if len(sys.argv) == 2 or len(sys.argv) == 3:
	subred = sys.argv[1]
	url = (URL_BASE + 'r/' + subred + '.json')
else:
	url = (URL_BASE + '.json')

# Try to get the url and time it
try:
	startTime = time.time()
	response = requests.get(url, headers = USER_AGENT)
	response.raise_for_status()
	elapsedTime = time.time() - startTime
	print('Got: "%s" in %s s' % (url, round(elapsedTime, 2)))
except requests.exceptions.RequestException as err:
	print(err)
	sys.exit(1)

# Load JSON data into a Python variable and get 'friendly' time stamp
theJSON = json.loads(response.text)
timeStamp = datetime.datetime.fromtimestamp(startTime).strftime('%Y.%m.%d_%H-%M-%S')


if len(sys.argv) == 3: # If passed a file arg, save the JSON
	jsonFile = sys.argv[2]
elif len(sys.argv) == 2:	# Elif save as subreddit with time stamp as JSON
	jsonFile = (sys.argv[1] + '_' + timeStamp + '.json')
else:	# Else we have the front page of reddit, save as JSON
	jsonFile = ('FrontPage_' + timeStamp + '.json')

# Save the JSON file
with open(jsonFile, 'w') as outfile:
		json.dump(theJSON, outfile)
