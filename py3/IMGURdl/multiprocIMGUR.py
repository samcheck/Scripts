import logging
import os
from time import time
from functools import partial
from multiprocessing.pool import Pool

from downloadIMGUR import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def main():
    ts =time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Could not find IMGUR_CLIENT_ID environment variable.")
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    download = partial(download_link, download_dir)
    with Pool(8) as p:
        p.map(download, links)
    logging.info('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
