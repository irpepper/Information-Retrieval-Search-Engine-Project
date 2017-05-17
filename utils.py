__author__="Jordan Sanders"
import os
import re
from nltk.stem.porter import *
import math
import cPickle
import bs4

def tokenize(doc):
    #Tokenize on whitespace and remove punctuation
    doc = re.sub(ur"\\n", "", str(doc))
    doc = re.sub(ur'((?<![0-9])[^a-zA-Z0-9\s])(?![0-9])', '', doc)
    doc = re.sub(ur"\s\s+", " ", doc.lower())
    doc = doc.split(" ")
    return doc

def remove_SGML(text):
    SGML = ["<DOC>", "<DOCNO>", "</DOCNO>", "<TITLE>", "</TITLE>", "<AUTHOR>", "</AUTHOR>", "<BIBLIO>", "</BIBLIO>", "<TEXT>", "</TEXT>", "</DOC>", "<table>","</tr>","<tr>","</td>","<td>"]
    for tag in SGML:
        text = re.sub(tag, "", str(text))

    return text


def get_stop_words():
    stop_words = open("stop_words.txt","r").readlines()
    stop_words = [x.replace("\n", "") for x in stop_words]

    return stop_words

def remove_stop_words(text):
    stop_words = get_stop_words()
    for word in stop_words:
        text = [x for x in text if x != word]

    return text

def porter_stemmer(text):
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(word) for word in text]
    return stemmed

def preprocess(text):
    text = remove_SGML(text)
    text = tokenize(text)
    text = remove_stop_words(text)
    text = porter_stemmer(text)
    if "" in text:
        text.remove("")
    if '' in text:
        text.remove('')

    text = [word[1:-1] if word[0] == "'" and word[-1] == "'" else word for word in text]
    return text


def tfidf_text(directory):
    docs = list()
    tf = dict()
    idf = dict()
    count = 0

    for f in os.listdir(directory):
        if f[0] != '.':
            print count
            count+=1
            html = cPickle.load(open(directory+str(f),"rb"))
            #Read document and preprocess into list of stemmed words
            text = preprocess(html)
            #Count the number of times each word appears in the document
            word_counts = dict()
            for word in text:
                if word in word_counts:
                    word_counts[word] += 1.0
                else:
                    word_counts[word] = 1.0

            #Get document vocab size
            unique_terms = len(set(text))

            #Add term frequency and document id to tf dictionary
            for word in set(text):
                if word not in tf:
                    tf[word] = list()
                tf[word].append((f[-4:],word_counts[word]/unique_terms))

    #Calculate idf for each word
    num_docs = len(os.listdir(directory))

    for word in tf.keys():
        idf[word] = math.log1p(num_docs/len(tf[word]))

    return tf, idf

def checkURL(url):
    if url == None:
        return False
    if url[-3:] == "mp3" or url[-3:] == "ppt":
        return False
    if not re.search(r"unt\.edu",url):
        return False
    if re.search(r".*(@)|(mailto:)|(\s)|(tel:).*",url):
        return False
    if re.search(r"\.[abcdefgijknopqrsuvwxyz]{3,4}$",url):
        return False
    return True

def fixURL(url):
    url = str(url)
    head = "http://"
    for i in range(len(head)):
        if url[i] != head[i]:
            url = url[:i] + head[i] + url[i:]

    url = re.sub(r"\.[html]{3,4}$", "", url)
    return url

def remove_html(soup):
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    text = re.sub(r"(\n)|(\t)", " ", text)
    return text
