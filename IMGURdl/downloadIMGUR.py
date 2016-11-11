# example from:
# https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import json
import logging
import os
from pathlib import Path
from urllib.request import urlopen, Request
# import requests

logger = logging.getLogger(__name__)

def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    url = 'https://api.imgur.com/3/gallery/random/random/'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # req = Request('https://api.imgur.com/3/gallery/random/random/', headers=headers, method='GET')
    # with urlopen(req) as resp:
    #     data = json.loads(resp.read().decode('utf-8'))
    return map(lambda item: item['link'], data['data'])


def download_link(directory, link):
    logger.info('Downloading %s', link)
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.read())


def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir
