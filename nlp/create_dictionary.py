from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk


# open the clean json
import json

testnum = 3
OUTPUT_PANTHEON = '../data/for_test.json'
CUSTOM = ['===']
STOPWORDS = set(stopwords.words('english') + CUSTOM)
DOCS = {}
RAW_TEXTS = []

import ijson  # or choose a faster backend if needed
from itertools import islice



with open(OUTPUT_PANTHEON) as f:
    parser = ijson.parse(f)
    ret = {'': {}}
    vals = {}
    counter = 0
    for prefix, event, value in parser:
        #print (prefix, event)
        if event == 'start_map':
            if not prefix:
                continue
            url = 'https://en.wikipedia.org/wiki?curid={}'.format(prefix)
            vals['url'] = url
        if prefix.endswith('.plain_txt'):
            words = word_tokenize(value)
            RAW_TEXTS.append([word for word in words if word not in STOPWORDS and len(word) > 2])
        if prefix.endswith('.full_name'):
            vals['name'] = value
        if event == 'end_map':
            DOCS[counter] = vals
            counter += 1
            vals = {}


print (DOCS)

from collections import defaultdict
frequency = defaultdict(int)
for text in RAW_TEXTS:
    for token in text:
        frequency[token] += 1

RAW_TEXTS = [[token for token in text if frequency[token] > 1] for text in RAW_TEXTS]

#from pprint import pprint
#pprint(RAW_TEXTS)

from gensim import corpora
dictionary = corpora.Dictionary(RAW_TEXTS)
dictionary.save('../data/all_data.dict')


corpus = [dictionary.doc2bow(text) for text in RAW_TEXTS]
corpora.MmCorpus.serialize('../data/allcorpus.mm', corpus)


from gensim import corpora, models, similarities
import os


dictionary = corpora.Dictionary.load('../data/TEST.dict')
corpus = corpora.MmCorpus('../data/testcorpus.mm')


tfidf = models.TfidfModel(corpus)

lsi = models.LsiModel(corpus)

corpus_tfidf = tfidf[corpus]
corpus_lsi = lsi[corpus]


index_tfidf = similarities.MatrixSimilarity(corpus_tfidf)
index_lsi = similarities.MatrixSimilarity(corpus_lsi)


import json


from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim import corpora, models, similarities
index_tmpfile = get_tmpfile("index")
index_all = similarities.Similarity(index_tmpfile, corpus_lsi, num_features=len(dictionary))


OUTPUT_RESULT = '/Users/lorynunez/scores_1.csv'

import csv
with open(OUTPUT_RESULT, 'w+') as w:
    csvwriter = csv.writer(w, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = ['Main_Name', 'Name', 'Score', 'URL']
    csvwriter.writerow(headers)
    for similarities in index_lsi:
        print ("START ======== ")
        sims = sorted(enumerate(similarities), key=lambda item: -item[1])
        name_counter = 0
        main_name = ''
        for sim in sims:
            to_write = []
            doc = DOCS.get(sim[0])
            if name_counter == 0:
                main_name = doc['name']
            to_write.append(main_name)
            to_write.append(doc['name'])
            to_write.append(sim[1])
            to_write.append(doc['url'])
            csvwriter.writerow(to_write)
            name_counter += 1
            #print('SCORE ', sim[1], ' ==> ', doc['name'], doc['url'])



