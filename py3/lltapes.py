
from bs4 import BeautifulSoup
import requests
import re
import sys


show_id = sys.argv[1]
URL_BASE = "http://www.lovelinetapes.com/shows/?id="
MP3_BASE = "http://recordings.lovelinetapes.com/"
url = (URL_BASE + show_id)
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# Find the URL elements
left_link = soup.find_all('a', attrs={'style': 'float: left;', 'class': 'showLink'})
right_link = soup.find_all('a', attrs={'style': 'float: right;', 'class': 'showLink'})
title = soup.find('title')
mp3 = soup.find('meta', attrs={'property': 'og:url'})

if left_link == []:
    print('Could not find link')
else:
    try:
        print(title.text)
        print(mp3['content'])
        print('Previous Show:')
        print(left_link[0].get('href'))
        print(left_link[0].find('div', attrs={'class': 'details'}).text.strip())
        print('Next Show:')
        print(right_link[0].get('href'))
        print(right_link[0].find('div', attrs={'class': 'details'}).text.strip())
    except requests.exceptions.MissingSchema:
        # skip this
        print('Could not find link')
