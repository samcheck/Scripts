
from bs4 import BeautifulSoup
import requests
import re
import sys
import os


show_id = sys.argv[1]
URL_BASE = "http://www.lovelinetapes.com/shows/?id="
MP3_BASE = "http://recordings.lovelinetapes.com/"
url = (URL_BASE + show_id)
exten = '.mp3'
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# Find the URL elements
left_link = soup.find_all('a', attrs={'style': 'float: left;', 'class': 'showLink'})
right_link = soup.find_all('a', attrs={'style': 'float: right;', 'class': 'showLink'})
title = soup.find('title')
page_url = soup.find('meta', attrs={'property': 'og:url'}) #full link w/ redirect to mp3 is in this meta tag
mp3_link = re.search(r'h\=\w+', page_url['content']).group().replace('h=', '') #match on the mp3 link format
url_ep = MP3_BASE + mp3_link + exten
title_date = re.search(r'\d?\d\/\d?\d\/\d{4}', title.text)
title_guest = re.search(r'\d{4}.*', title.text)

def save_ep(show_id):
    url = (URL_BASE + show_id)
    exten = '.mp3'
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find('title')
    title_date = re.search(r'\d?\d\/\d?\d\/\d{4}', title.text)
    title_guest = re.search(r'\d{4}.*', title.text)
    mp3_link = re.search(r'h\=\w+', page_url['content']).group().replace('h=', '') #match on the mp3 link format
    url_ep = MP3_BASE + mp3_link + exten

    save_name = ("Loveline - " + title_date.group().replace('/', '-') +
                re.sub(r'\d{4}', '', title_guest.group()) + exten)
    curpath = os.path.abspath(os.curdir)
    # Download the episode
    print('Downloading %s...' % url_ep)
    r = requests.get(url_ep, stream=True)
    r.raise_for_status()
    if r.status_code == 200:
        print('Saving as %s' % save_name)
        with open(os.path.join(curpath, save_name), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


if left_link == []:
    print('Could not find link')
else:
    try:
        print(title.text)
        if title_guest is not None:
            print('Guest: ' + re.sub(r'\d{4} - ', '', title_guest.group()))
        if title_date is not None:
            print('Date: ' + title_date.group())
        print(url_ep)
        print('\nPrevious Show:')
        print(left_link[0].get('href'))
        print(left_link[0].find('div', attrs={'class': 'details'}).text.strip())
        print('\nNext Show:')
        print(right_link[0].get('href'))
        print(right_link[0].find('div', attrs={'class': 'details'}).text.strip())
        if len(sys.argv) == 3:
            if sys.argv[2] == 'd':
                save_ep(show_id)
    except requests.exceptions.MissingSchema:
        # skip this
        print('Could not find link')
