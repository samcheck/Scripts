#!/usr/bin/env python3
# bing_background.py - downoads the bing homepage background and sets it as the
#                      desktop backgroud.

import logging
import os
from urllib.request import urlopen
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display


def download_link(directory, link):
    download_path = os.path.join(directory, os.path.basename(link))
    # Check if file already exists
    if os.path.exists(download_path):
        logging.info('File {} already exists, skipping.'.format(link))
    else:
    # Download the img
        logging.info('Downloading {}'.format(link))
        with urlopen(link) as image, open(download_path, 'wb') as f:
            f.write(image.read())


def change_wp(directory, link):
    # Changes wallpaper for Unity / Gnome desktop
    desktop = os.environ.get("DESKTOP_SESSION")
    if desktop in ["gnome", "ubuntu", "unity"]:
        img_path = os.path.join(directory, os.path.basename(link))
        command = "gsettings set org.gnome.desktop.background picture-uri file://{}".format(img_path)
        os.system(command)
    else:
        logging.error('No command to change wallpaper.')


def setup_download_dir(save_dir):
    download_dir = os.path.join(os.getcwd(), save_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    return download_dir


def main():
    # set up logging
    logging.basicConfig(filename='bing_bg.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    url = "https://www.bing.com/"
    save_dir = "images"
    dl_dir = setup_download_dir(save_dir)

    # set up a virtual display to use with selenium
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Launch a Firefox instance
    driver = webdriver.Firefox()
    driver.get(url)
    logging.info('Downloading page {}'.format(url))
    time.sleep(6) #hacky sleep to allow bing homepage to load so we can grab the image

    # Parse the bing homepage
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # clean up browser and stop virtual display
    driver.quit() # seems to spit out "'NoneType' object has no attribute 'path'"
    display.stop()

    # Find the URL elements
    link = soup.find_all('div', {'id': 'bgDiv'})[0].attrs['style']
    img_link = link[(link.find('url("')+5):link.find('");')]
    logging.info('Found link: {}'.format(img_link))

    # Download and change wallpaper
    download_link(dl_dir, img_link)
    change_wp(dl_dir, img_link)


if __name__ == "__main__":
    main()
