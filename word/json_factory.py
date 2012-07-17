# Custom Corpus Loader using NLTK
# Paul E Williams and Michael Odland 2012
# last modified 5/17/2012 pew

# todo:
# format and load single-column CSV [ x ]
# tokenize data by row, sentence, and word [ x ]
# pass off corpus to word frequency distribution fnctn [ x ]
# export data as json file to send to django server [ x ]
# party [  ]
from fileinput import filename

import nltk
import nltk.data
import csv, re
import json
import simplejson
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from django.core.files import File
from word.models import *


def json_file(data_string, filename, fcnname ):
    """
    jsonEncoded data_string in, filename, and function name in
    json file out
    naming convention for json files:
        "filename(including ext).functionname.json"
    """
    print "TEST: json_file call"
    data = []
    data.append(data_string)
    f = open((str(filename) + '.' + str(fcnname) + ".json"), "w+")
    json.dump(data, f, separators=('},{',', '))

    f.flush()
    print "TEST: successful json dump and flush"
    return data_string


def json_encode(dic):
    """
    dictionary in
    json object out
    """
    print "TEST: json_encode call"

    data = []
    data.append(dic)
    data_string = json.dumps(data)
    print "TEST: json encoded ", data_string

    return data_string


def vocabulary(wordcount):
    """
    alphabetized vocabulary built using list comprehension.
    """
    print "TEST: vocabulary call"

    vocab = sorted( [word for word in wordcount.keys()] )

    return vocab


def pull_stops(text):
    """
    Stopwords are rarely useful in information retrieval tasks. Removing them is common.
    This list of english stops is taken from the nltk english stopswords file.
    """
    print "TEST: pull_stops call"

    english_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
                     'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                     'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
                     'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
                     'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                     'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                     'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                     'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                     'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
                     'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
                     'will', 'just', 'don', 'should', 'now']
    text2 = []
    for word in text:
        lower = word.lower()
        if lower.isalpha() and lower not in english_stops:
            text2.append(lower)

    return text2


def lemma(words):
    """
    lematization is very similar to stemming but more
    akin to synonym replacement. A lemma is a root word and so a valid
    word (rather than a stem) is always returned. If lemmatizer does not
    find a root word it simply returns the original.
    """
    print "TEST lemma call"

    words2 = []
    for w in words:
        words2.append(lemmatizer.lemmatize(w))

    return words2


#todo: in important_words m and n should become parameters set by the user. Current test case has them hard coded.
def important_words(wordcount, vocab):
    """
    if a word in a texts vocabulary has more than m letters and occurs more than n times
    include it in the important dictionary.
    """
    print "TEST: important_words call"



    return dict(  [w, (wordcount[w]) ]  for w in vocab if len(w) > 3 and wordcount[w] > 3  )



def corpus_reader(filepath):
    """
    takes a filepath including filename
    formats in case file is csv
    loads file into PlainTextCorpusReader
    """
    print "TEST: corpus_reader call"

    csv_file = open(filepath, 'rb') # use test_1.csv as test case
    csv_data = csv.reader(csv_file)
    global csv_read
    csv_read = open('uploads/tmp/read.tmp', 'w')
    for line in csv_data:
        line_to_write = re.sub('[\s\t]+', ' ', str(line))
        line_to_write = line_to_write.lstrip('[\'')
        line_to_write = line_to_write.rstrip('\']')
        csv_read.write(str(line_to_write) + "\n\n")
    root = 'uploads/'
    corpus = PlaintextCorpusReader(root, 'tmp/read.tmp')
    #response = corpus.paras()
    words = corpus.words()
    return words


def process(filepath):
    print "TEST: process call"
    text        = corpus_reader(filepath)
    stop_free   = pull_stops(text)
    wordcount   = nltk.FreqDist(stop_free)
    vocab       = vocabulary(wordcount)
    print "TEST: unformatted vocab is" + repr(vocab)
    important   = important_words(wordcount, vocab)
    print "TEST: important is " + repr(important)
    json_file(important, filepath, 'important')
    return filepath
#EOF
