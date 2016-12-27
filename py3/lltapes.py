#!/usr/bin/python3
# lltapes.py - Uses BeautifulSoup and requests to parse and download episodes
#              from lovelinetapes.

import re
import sys
import os
import logging
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup

URL_BASE = "http://www.lovelinetapes.com/shows/"
EXTEN = '.mp3'
CHUNK_SIZE = 1024*8

class DownloadWorker(Thread):
    """Saves episodes by show_id from queue"""
    def __init__(self, queue):
        super(DownloadWorker, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            show_id = self.queue.get()
            save_ep(show_id)
            self.queue.task_done()


def get_page(show_id):
    """Uses bs4 to get the page of a given Loveline episode by show_id.

    Argument:
        show_id: numeric id (as string) from Loveline Tapes site.

    Returns:
        BeautifulSoup object of the page, decoded with lxml.
    """

    url = (URL_BASE + '?id=' + show_id)
    logging.info('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    return BeautifulSoup(res.text, "lxml")


def get_year_links(year):
    """Uses bs4 to get show_ids for all episodes in a given year.

    Argument:
        year: a year (as string) to search the Loveline Tapes site.
        soup: optional BeautifulSoup object to search.

    Returns:
        List containing strings of show_ids in the given year.
    """

    url = (URL_BASE + 'browse/?y=' + year)
    logging.info('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    # Find the URL elements
    links = soup.find_all('a', attrs={'class': 'showLink'})
    show_id, show_info = [], []
    for link in links:
        show_id.append(link.get('href').replace('/shows/?id=', ''))
        #show_info.append(link.find('div', attrs={'class': 'details'}).text.strip().split('\n'))
    return show_id


def get_mp3_url(show_id, soup=None):
    """Uses bs4 to get link to mp3 recording of Loveline episode.

    Argument:
        show_id: numeric id (as string) from Loveline Tapes site.
        soup: optional BeautifulSoup object to search.

    Returns:
        String of the link to mp3 recording.
    """

    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    page_url = soup.find('meta', attrs={'property': 'og:url'}) #full link w/ redirect to mp3 is in this meta tag
    if re.search(r'h\=\w+', page_url['content']) is None:
        mp3_link = None
        url_ep = None
    else:
        mp3_link = re.search(r'h\=\w+', page_url['content']).group().replace('h=', '') #match on the mp3 link format
        url_ep = "http://recordings.lovelinetapes.com/" + mp3_link + EXTEN

    return url_ep


def get_page_title(show_id, soup=None):
    """Uses bs4 to get guest and date of Loveline episode.

    Argument:
        show_id: numeric id (as string) from Loveline Tapes site
        soup: optional BeautifulSoup object to search

    Returns:
        Dictionary containing guest, year, month and day as strings.
        Month and day are zero padded.
    """

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
    """Uses requests to download an mp3 recording of a Loveline episode.
    Checks to determine if the episode already exists and is of expected size.

    Argument:
        show_id: numeric id (as string) from Loveline Tapes site.
        soup: optional BeautifulSoup object to search.

    Returns:
        Nothing, downloads episode to current directory.
    """
    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    url_ep = get_mp3_url(show_id, soup)
    title = get_page_title(show_id, soup)
    date = title['year'] + '-' + title['month']+ '-' + title['day']
    name = ('Loveline - ' + date + ' (Guest - ' + title['guest'] + ')' + EXTEN)
    save_name = safe_name(name)
    curpath = os.path.abspath(os.curdir)

    # Download the episode
    if url_ep is not None:
        logging.info('Downloading {}'.format(url_ep))
        r = requests.get(url_ep, stream=True)
        r.raise_for_status()
        size = int(r.headers['Content-Length'])
        if os.path.isfile(save_name) and (os.path.getsize(save_name) == size):
            # check if file already exists and is of the expected size
            # can still replace interupted downloads
            logging.warning('Episode already downloaded, skipping.')
        else:
            if r.status_code == 200:
                logging.info('Saving as: {}'.format(save_name))
                logging.info('Expected file size: {} bytes'.format(size))
                with open(os.path.join(curpath, save_name), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        f.write(chunk)
            else:
                logging.warning('Problem loading page: HTML response code {}'.format(r.status_code))
    else:
        logging.warning('Episode url not found')


def safe_name(save_name):
    safe_name = save_name.replace('/', ' ')
    return safe_name


def find_link(show_id, direction, soup=None):
    """Uses bs4 to find links to next or previous episodes from current show id
    of Loveline episode.

    Argument:
        show_id: numeric id (as string) from Loveline Tapes site.
        soup: optional BeautifulSoup object to search.

    Returns:
        None if direction is not 'left' or 'right'
        Dictionary containing direction of link, show id, show guest, and show date.
    """

    if not isinstance(soup, BeautifulSoup):
        soup = get_page(show_id)

    # Find the URL elements
    if direction == 'left' or 'right':
        link = soup.find_all('a', attrs={'style': 'float: {};'.format(direction), 'class': 'showLink'})
    else:
        return None

    show_id = link[0].get('href').replace('/shows/?id=', '')
    show_info = link[0].find('div', attrs={'class': 'details'}).text.strip().split('\n')

    return{'direction': direction, 'show_id': show_id, 'show_guest': show_info[0], 'show_date': show_info[1]}


def main():
    logging.basicConfig(filename='lltapes.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logger = logging.getLogger(__name__)
    if len(sys.argv) > 2:
        show_id = sys.argv[1]
        soup = get_page(show_id)
        links = find_link(show_id, 'right', soup)
        url_ep = get_mp3_url(show_id, soup)
        title = get_page_title(show_id, soup)
        if title['guest'] is None:
            logging.warning('Could not find show.')
        else:
            try:
                logging.info('Guest: ' + title['guest'])
                if title['year'] is not None:
                    logging.info('Date: ' + title['year'] + '-' + title['month']+ '-' + title['day'])
                logging.info(url_ep)
                logging.info(links)
                if len(sys.argv) == 3:
                    if sys.argv[2] == 'd':
                        save_ep(show_id, soup)
            except requests.exceptions.MissingSchema:
                # skip this
                logging.warning('Could not find show.')

    elif len(sys.argv) == 2:
        year = get_year_links(sys.argv[1])
        # Create a Queue to communicate with the worker threads
        queue = Queue()
        # Create 8 worker threads
        for x in range(4):
            worker = DownloadWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()
        # Put tasks into the queue as tuples
        for show_id in year:
            logger.info('Queueing {}'.format(show_id))
            queue.put(show_id)
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()

if __name__ == "__main__":
    main()
