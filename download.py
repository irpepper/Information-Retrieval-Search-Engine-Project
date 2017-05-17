__author__ = "Jordan Sanders"
"""
Final Project
Search Engine
CSCE 5200

Webpage downloader
"""

from utils import checkURL, fixURL, remove_html
import cPickle
from bs4 import BeautifulSoup
from bs4 import element
import bs4
from Queue import Queue
import urllib2
import re
from urlparse import urlparse
import html2text

def main():
    #Parameters
    START = "http://www.unt.edu"
    DOC_LIMIT = 3000
    OUT_FILE = "html_downloads/"
    count = 0

    #Queue class for breadth-first Search
    queue = Queue()
    #Populate first starting address
    queue.put(START)

    #List of visited websites
    visited = list()

    #Download pages
    while (not queue.empty() and count < DOC_LIMIT):
        url = queue.get()
        try: response = urllib2.urlopen(url)
        except urllib2.URLError:
            continue
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all('a'):
            link = link.get('href')
            if checkURL(link):
                try:link = fixURL(link)
                except:
                    continue
                if (link not in visited):
                    queue.put(link)
                    visited.append(link)

        print url + " " + str(count)
        try:
            text = remove_html(soup)
            cPickle.dump((url,text),open(OUT_FILE+str(count),"wb"))
            count += 1
        except:
            continue






if __name__ == '__main__':
    main()
