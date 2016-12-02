#! python3
# dlTAL.py - Downloads a specific range of "This American Life" eps

import requests, os
from bs4 import BeautifulSoup

# Starting URL
url = 'http://audio.thisamericanlife.org/jomamashouse/ismymamashouse/'
url_title = 'http://www.thisamericanlife.org/radio-archives/episode/'

# Range
dl_start = 525
dl_end = 525
exten = '.mp3'

# Place to store podcasts
os.makedirs('TAL', exist_ok=True)

for ep in range(dl_start, (dl_end + 1)):

	# Create unique URL for each episode
	url_ep = url + str(ep) + exten
	url_name = url_title + str(ep)
	
	# Pull name of episode
	res = requests.get(url_name)
	res.raise_for_status()
	soup = BeautifulSoup(res.text, 'html.parser')
	# Find title and extract w/ clean up of ':'
	save_name = soup.find('h1', class_='node-title').string.replace(':','')
	
	# Download the episode
	print('Downloading %s...' % url_ep)
	res = requests.get(url_ep)
	res.raise_for_status()
	
	# Save the file to ./TAL
	audio_file = open(os.path.join('TAL', '#' + save_name + exten), 'wb')
	for chunk in res.iter_content(100000):
		audio_file.write(chunk)
	audio_file.close()
	
print('Done.')
