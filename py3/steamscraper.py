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
    logging.info('Downloading page {}'.format(url))
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

    # Check if there are no matches and return
    no_match = soup.find_all('div', class_="market_listing_table_message")
    if no_match and "There were no items matching your search" in no_match[0].get_text():
        logging.info('No match for search: {}'.format(term))
        return 0

    # Get item stats from search result
    volume = soup.find_all('span', class_="market_listing_num_listings_qty")
    sale_price = soup.find_all('span', class_="sale_price")
    item_name = soup.find_all('span', class_="market_listing_item_name")
    game_name = soup.find_all('span', class_="market_listing_game_name")

    # Create objects for each item found
    obj = []
    for i in range(len(volume)):
        obj.append(SteamItem(item_name[i].get_text(), sale_price[i].get_text(),
                                volume[i].get_text(), game_name[i].get_text()))

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
        if out == 0:
            print("No matches for search: {}".format(term))
        else:
            for item in out:
                item.display()

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
