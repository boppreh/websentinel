import argparse
import requests
import time
import simplecrypto
import webbrowser

try:
    parser = argparse.ArgumentParser(description='Watches webpages for changes.')
    parser.add_argument('urls', metavar='W', type=str, nargs='+',
                        help='list of urls to be monitored')
    parser.add_argument('--keyword', metavar='K', type=str, nargs='+',
                        help='list of keywords expected in the webpages')

    args = parser.parse_args()
    urls = args.urls
    keywords = args.keywords
except:
    print '\nFalling back to interactive mode.\n'
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

    def update(self, keywords):
        content = requests.get(self.url).content
        for keyword in keywords:
            if not keyword in content:
                return

        new_hash = simplecrypto.hash(content)
        if new_hash != self.previous_hash:
            webbrowser.open(self.url)
            self.previous_hash = new_hash


sentinels = map(Sentinel, urls)
while True:
    for sentinel in sentinels:
        sentinel.update(keywords)

    time.sleep(30)
