__author__ = "Jordan Sanders"
"""
Final Project
Search Engine
CSCE 5200

Create vector space model
"""

from utils import tfidf_text, preprocess
import cPickle
from bs4 import BeautifulSoup
from Queue import Queue
import urllib2
import re
from urlparse import urlparse


def main():
    directory = "html_downloads/"
    fp = open("tfidf.pickle","wb")
    tf, idf = tfidf_text(directory)
    cPickle.dump(tf, fp)
    cPickle.dump(idf, fp)



if __name__ == '__main__':
    main()
