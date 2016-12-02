# example from:
# https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import logging
import os
from time import time
from queue import Queue
from threading import Thread

from downloadIMGUR import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

class DownloadWorker(Thread):
    """docstring for DownloadWorker."""
    def __init__(self, queue):
        super(DownloadWorker, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Could not find IMGUR_CLIENT_ID environment variable.")
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    # Create a Queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put tasks into the queue as tuples
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logger.info('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
