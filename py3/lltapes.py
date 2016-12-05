
from bs4 import BeautifulSoup
import requests


URL_BASE = "http://www.lovelinetapes.com/shows/?id=1724"
MP3_BASE = "http://recordings.lovelinetapes.com/ZmVmZWIyZDg.mp3"
print('Downloading page %s...' % URL_BASE)
res = requests.get(URL_BASE)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# Find the URL of the comic img
left_link = soup.find_all('a', attrs={'style': 'float: left;', 'class': 'showLink'})
right_link = soup.find_all('a', attrs={'style': 'float: right;', 'class': 'showLink'})
#print(elem)
if left_link == []:
    print('Could not find link')
else:
    try:
        print(left_link[0].get('href'))
        print(left_link[0].find('div', attrs={'class': 'details'}).text.strip())
        print('\n')
        print(right_link[0].get('href'))
        print(right_link[0].find('div', attrs={'class': 'details'}).text.strip())
    except requests.exceptions.MissingSchema:
        # skip this
        print('Could not find link')
