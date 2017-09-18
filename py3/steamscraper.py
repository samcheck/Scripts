import logging
import argparse
import sys

import requests
from bs4 import BeautifulSoup

URL_BASE = "https://steamcommunity.com/market/search?"

class SteamItem(object):
    """Class to hold info about items on Steam Market"""
    def __init__(self, name, buyer_price, seller_price, volume, game):
        self.name = name
        self.buyer_price = float(buyer_price[1:])
        self.seller_price = float(seller_price[1:])
        self.steam_cut = round(self.buyer_price - self.seller_price, 2)
        self.volume = volume
        self.game = game

    def display(self):
        print("Name: {}".format(self.name))
        print("Buyer Pays Price: ${}".format(self.buyer_price))
        print("Seller Recieves Price: ${}".format(self.seller_price))
        print("Steam Commission: ${}".format(self.steam_cut))
        print("Volume: {}".format(self.volume))
        print("Game: {}".format(self.game))
        print("-"*40)


class SteamGame(object):
    """Class to hold info about games on Steam Market"""
    def __init__(self, name, app_id):
        self.name = name
        self.app_id = app_id

    def display(self):
        print("Name: {}".format(self.name))
        print("Steam App ID: {}".format(self.app_id))
        print("-"*40)


def get_page(term):
    """Uses bs4 to get the page of a given search term.

    Argument:
        term: string to search for.

    Returns:
        BeautifulSoup object of the page, decoded with lxml.
    """

    url = (URL_BASE + 'q=' + term)
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
    norm_price = soup.find_all(lambda tag: tag.name == 'span' and
                                   tag.get('class') == ['normal_price'])

    sale_price = soup.find_all('span', class_="sale_price")
    item_name = soup.find_all('span', class_="market_listing_item_name")
    game_name = soup.find_all('span', class_="market_listing_game_name")

    # Create objects for each item found
    obj = []
    for i in range(len(volume)):
        obj.append(SteamItem(item_name[i].get_text(), norm_price[i].get_text(),
                            sale_price[i].get_text(), volume[i].get_text(),
                            game_name[i].get_text()))

    return obj


def get_games(soup=None):
    """Uses bs4 to get list of games on Steam Marketplace.

    Argument:
        (Optionally) soup: bs4 object to search on.

    Returns:
        Array of objects, containing all games on marketplace.
    """

    if not isinstance(soup, BeautifulSoup):
        soup = get_page('') #empty search

    games = soup.select('div[data-appid]')
    # Create objects for each item found
    obj = []
    for i in range(len(games)):
        obj.append(SteamGame(games[i].find('span').get_text(),
                            games[i]['data-appid']))

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
    parser.add_argument('-g', '--game', help='Game to search, default search entire market', default=None)
    parser.add_argument('-l', '--list', help='List games on steam marketplace to search', action='store_true')

    args = parser.parse_args()

    # optionally list the games that can be searched on the marketplace
    if args.list:
        game_list = get_games()
        for item in game_list:
            item.display()

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
