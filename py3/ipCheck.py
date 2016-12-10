#!/usr/bin/python3
# ipCheck.py - returns geo-ip information for current IP

import json, requests

# Download the JSON data from http://freegeoip.net/json/
url ='http://freegeoip.net/json/'
response = requests.get(url)
response.raise_for_status()

# Load JSON data into a Python variable and print
ipData = json.loads(response.text)
print('Current IP:', ipData['ip'])
print('Current IP location:', ipData['city'], ipData['country_name'])
