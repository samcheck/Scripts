#!/usr/bin/python3

import logging
import os
from urllib.request import urlopen
import time

from bs4 import BeautifulSoup
from selenium import webdriver

logger = logging.getLogger(__name__)

def download_link(directory, link):
    logger.info('Downloading %s', link)
    download_path = os.path.join(directory,os.path.basename(link))
    # Download the img
    with urlopen(link) as image, open(download_path, 'wb') as f:
        f.write(image.read())


url = "http://www.bing.com/"
dl_dir = os.getcwd()
logging.info('Downloading page %s...' % url)
driver = webdriver.Firefox()
driver.get(url)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Find the URL elements
link = soup.find_all('div', {'id': 'bgDiv'})[0].attrs['style']
img_link = link[(link.find('url("')+5):link.find('");')]

download_link(dl_dir, img_link)
