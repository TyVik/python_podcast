from pathlib import Path

import requests
from lxml import etree


SITES = {
    'Python bytes': 'https://pythonbytes.fm', 
    'Talk python to me': 'https://talkpython.fm'
}


def download(site, url):
    path_mp3 = f'{site}/mp3'
    path = Path(path_mp3)
    path.mkdir()
    response = requests.get(f'{url}/episodes/all')
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(response.text, htmlparser)
    for episode in tree.xpath('//table//tr//a'):
        # print(episode.attrib['href'].replace('show', 'transcript'))
        link = episode.attrib['href'].split('/')
        name = link[-1]
        index = link[-2]
        print(name)
        mp3 = requests.get(f'{url}/episodes/download/{index}/{name}.mp3')
        with open(f'{path_mp3}/{index} - {name}.mp3', 'wb') as f:
            f.write(mp3.content)


if __name__ == '__main__':
    for site, url in SITES.items():
        Path(site).mkdir()
        download(site, url)
