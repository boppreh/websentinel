import argparse
import requests
import time
import simplecrypto
import webbrowser
import os

try:
    parser = argparse.ArgumentParser(description='Watches webpages for changes.')
    parser.add_argument('urls', metavar='W', type=str, nargs='+',
                        help='list of urls to be monitored')
    parser.add_argument('-k', '--keyword', metavar='K', type=str, nargs='+',
                        help='list of keywords expected in the webpages')
    parser.add_argument('-c', '--command', metavar='c', type=str, nargs='+',
                        help='system command executed ')

    args = parser.parse_args()
    urls = args.urls
    keywords = args.keyword
    command = args.command
except:
    print('\nFalling back to interactive mode.\n')
    def get_sequence(prompt):
        while True:
            url = raw_input(prompt)
            if not url: return
            yield url

    urls = list(get_sequence('URL: '))
    keywords = list(get_sequence('Keyword: '))


class Sentinel(object):
    def __init__(self, url):
        if not url.startswith('http'):
            url = 'http://' + url

        self.url = url
        self.previous_hash = ''

    def update(self, keywords, command=None):
        content = requests.get(self.url).content
        for keyword in keywords:
            if not keyword in content:
                return

        new_hash = simplecrypto.hash(content)
        if new_hash != self.previous_hash:
            if command:
                os.system(command)
            else:
                webbrowser.open(self.url)
            self.previous_hash = new_hash


sentinels = map(Sentinel, urls)
while True:
    for sentinel in sentinels:
        sentinel.update(keywords, command)

    time.sleep(30)
