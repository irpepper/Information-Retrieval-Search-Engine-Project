__author__ = "Jordan Sanders"
from utils import tfidf_text, preprocess
import os
import cPickle
from optparse import OptionParser


def main():
    print "Please enter a query: "
    query = raw_input()
    while query != "no":
        directory = "html_downloads/"
        #if tf and idf objects are stored, use them
        if os.path.isfile("tfidf.pickle"):
            fp = open("tfidf.pickle","rb")
            tf = cPickle.load(fp)
            idf = cPickle.load(fp)
        #else error
        else:
            print "No tfidf calculated, run make_model.py"
            return 0

        #Preprocess query
        query = preprocess(query.split(" "))

        #Sum tfidf^2 for each document
        similarity = dict()
        for word in query:
            if word in tf:
                for tup in tf[word]:
                    if tup[0] not in similarity:
                        similarity[tup[0]] = 0.0
                    similarity[tup[0]] += (tup[1] * idf[word])**2

        #Square root final sum for each document
        for key in similarity.keys():
            similarity[key] **= 0.5

        #Print sorted query rankings in descending order
        rankings = sorted(similarity, key=similarity.get, reverse=True)
        count = 1
        for doc in rankings:
            print str(count) + " " + cPickle.load(open(directory+str(doc),"rb"))[0]
            count += 1
            if count == 6:
                break
        print "If you'd like to quit, type no, else enter a search query: "
        query = raw_input()
        #recall = Number of relevant documents retrieved / Total number of relevant documents
        #precision = Number of relevant documents retrieved / Total number of documents retrieved




if __name__ == '__main__':
    main()
