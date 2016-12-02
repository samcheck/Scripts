#!/usr/bin/python3
# jsonRedditParse.py - loads previously saved Reddit JSON data 
# Usage: jsonRedditParse.py <json_file_to_load>

import sys, json, pprint


# Load JSON data into a Python variable and print
if len(sys.argv) == 2:
	with open(sys.argv[1]) as data_file:
		jsonData = json.load(data_file)

	# working off of Reddit JSON formatted data and get urls
	for child in jsonData['data']['children']:
		pprint.pprint(child['data']['url'])

else:
	print('Usage: jsonParse.py <json_file_to_load>')
