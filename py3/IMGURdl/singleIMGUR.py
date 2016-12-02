# example from:
# https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import logging
import os
from time import time

from downloadIMGUR import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Could not find IMGUR_CLIENT_ID environment variable.")
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    for link in links:
        download_link(download_dir, link)
    logger.info('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
