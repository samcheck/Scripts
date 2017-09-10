import re
import logging
import argparse

import requests
from bs4 import BeautifulSoup

URL_BASE = "https://steamcommunity.com/market/search?appid=730"

class SteamItem(object):
    """Class to hold info about items on Steam Market"""
    def __init__(self, name, price, volume, game):
        self.name = name
        self.price = price
        self.volume = volume
        self.game = game

    def display(self):
        print("Name: {}".format(self.name))
        print("Price: {}".format(self.price))
        print("Volume: {}".format(self.volume))
        print("Game: {}".format(self.game))
        print("-"*40)


def get_page(term):
    """Uses bs4 to get the page of a given search term.

    Argument:
        term: string to search for.

    Returns:
        BeautifulSoup object of the page, decoded with lxml.
    """

    url = (URL_BASE + '&q=' + term)
    logging.info('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    return BeautifulSoup(res.text, "lxml")


def get_details(term, soup=None):
    """Uses bs4 to get details of a steam market item.

    Argument:
        term: string to search for.
        soup: optional BeautifulSoup object to search.

    Returns:
        array of objects
    """

    if not isinstance(soup, BeautifulSoup):
        soup = get_page(term)

    volume = soup.find_all('span', class_="market_listing_num_listings_qty")
    sale_price = soup.find_all('span', class_="sale_price")
    item_name = soup.find_all('span', class_="market_listing_item_name")
    game_name = soup.find_all('span', class_="market_listing_game_name")

    obj = []
    for i in range(len(volume)):
        vol = str(volume[i]).replace('<span class="market_listing_num_listings_qty">', '').replace('</span>', '')
        price = str(sale_price[i]).replace('<span class="sale_price">', '').replace('</span>', '')
        name = re.search(r';">.+', str(item_name[i])).group().replace(';">', '').replace('</span>', '')
        game = str(game_name[i]).replace('<span class="market_listing_game_name">', '').replace('</span>', '')
        obj.append(SteamItem(name, price, vol, game))

    return obj


def main():
    # set up logging
    logging.basicConfig(filename='sscrape.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logger = logging.getLogger(__name__)

    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='Search term.')
    args = parser.parse_args()

    if args.search:
        term = args.search
        out = get_details(term)
        for item in out:
            item.display()

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
