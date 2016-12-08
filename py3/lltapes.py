


import re
import sys
import os

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

URL_BASE = "http://www.lovelinetapes.com/shows/?id="
MP3_BASE = "http://recordings.lovelinetapes.com/"
EXTEN = '.mp3'
CHUNK_SIZE = 1024

def get_page(show_id):
    url = (URL_BASE + show_id)

    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    return BeautifulSoup(res.text, "lxml")


def get_mp3_url(show_id, soup=None):
    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    page_url = soup.find('meta', attrs={'property': 'og:url'}) #full link w/ redirect to mp3 is in this meta tag
    if re.search(r'h\=\w+', page_url['content']) is None:
        mp3_link = None
        url_ep = None
    else:
        mp3_link = re.search(r'h\=\w+', page_url['content']).group().replace('h=', '') #match on the mp3 link format
        url_ep = MP3_BASE + mp3_link + EXTEN

    return url_ep


def get_page_title(show_id, soup=None):
    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    title = soup.find('title')

    title_date = re.search(r'\d?\d\/\d?\d\/\d{4}', title.text) # no matches if not a valid id
    if title_date is None:
        title_month, title_day, title_year = None
    else:
        title_month = title_date.group().split('/')[0].zfill(2)
        title_day = title_date.group().split('/')[1].zfill(2)
        title_year = title_date.group().split('/')[2]

    title_guest = re.search(r'\d{4}.*', title.text) # no matches if not a valid id
    if title_guest is None:
        guest = None
    else:
        guest = re.sub(r'\d{4} - ', '', title_guest.group())

    return{'guest': guest, 'year': title_year, 'month': title_month, 'day': title_day}


def save_ep(show_id, soup=None):
    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    url_ep = get_mp3_url(show_id, soup)
    title = get_page_title(show_id, soup)
    date = title['year'] + '-' + title['month']+ '-' + title['day']
    save_name = ('Loveline - ' + date + ' - ' + title['guest'] + EXTEN)

    curpath = os.path.abspath(os.curdir)
    # Download the episode
    if url_ep is not None:
        print('Downloading %s...' % url_ep)
        r = requests.get(url_ep, stream=True)
        r.raise_for_status()
        size = int(r.headers['Content-Length'])
        if r.status_code == 200:
            print('Saving as %s' % save_name)
            with open(os.path.join(curpath, save_name), 'wb') as f:
                for chunk in tqdm(r.iter_content(chunk_size=CHUNK_SIZE), total=size/CHUNK_SIZE, unit='kb'):
                    f.write(chunk)
    else:
        print('Warning: ep url not found')

def main():
    show_id = sys.argv[1]
    soup = get_page(show_id)

    # Find the URL elements
    left_link = soup.find_all('a', attrs={'style': 'float: left;', 'class': 'showLink'})
    right_link = soup.find_all('a', attrs={'style': 'float: right;', 'class': 'showLink'})

    url_ep = get_mp3_url(show_id, soup)
    title = get_page_title(show_id, soup)

    if title['guest'] is None:
        print('Could not find show.')
    else:
        try:
            print('Guest: ' + title['guest'])
            if title['year'] is not None:
                print('Date: ' + title['year'] + '-' + title['month']+ '-' + title['day'])
            print(url_ep)
            print('\nPrevious Show:')
            print(left_link[0].get('href'))
            print(left_link[0].find('div', attrs={'class': 'details'}).text.strip())
            print('\nNext Show:')
            print(right_link[0].get('href'))
            print(right_link[0].find('div', attrs={'class': 'details'}).text.strip().split('\n'))
            if len(sys.argv) == 3:
                if sys.argv[2] == 'd':
                    save_ep(show_id, soup)
        except requests.exceptions.MissingSchema:
            # skip this
            print('Could not find show.')

if __name__ == "__main__":
    main()
