#!/usr/bin/python3

import logging
import os
from urllib.request import urlopen
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def download_link(directory, link):
    logging.info('Downloading %s', link)
    download_path = os.path.join(directory, os.path.basename(link))
    # Download the img
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
    logging.basicConfig(filename='bing_bg.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    url = "http://www.bing.com/"
    save_dir = "images"
    dl_dir = setup_download_dir(save_dir)

    driver = webdriver.Firefox()
    driver.get(url)
    logging.info('Downloading page %s...' % url)
    time.sleep(3) #hacky sleep to allow bing homepage to load so we can grab the image
    # Parse the bing homepage
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit() # seems to spit out "'NoneType' object has no attribute 'path'"

    # Find the URL elements
    link = soup.find_all('div', {'id': 'bgDiv'})[0].attrs['style']
    img_link = link[(link.find('url("')+5):link.find('");')]

    # Download and change wallpaper
    download_link(dl_dir, img_link)
    change_wp(dl_dir, img_link)


if __name__ == "__main__":
    main()
