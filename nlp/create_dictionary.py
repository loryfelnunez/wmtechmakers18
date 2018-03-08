from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk


# open the clean json
import json

testnum = 3
OUTPUT_PANTHEON = '../data/for_test.json'
CUSTOM = ['===']
STOPWORDS = set(stopwords.words('english') + CUSTOM)

RAW_TEXTS = []

with open(OUTPUT_PANTHEON, 'r+') as orgfile:
    json_data = json.load(orgfile)
    for key, val in json_data.items():
        plain_text = val.get('plain_txt')
        words = word_tokenize(plain_text)
        RAW_TEXTS.append([word for word in words if word not in STOPWORDS and len(word) > 2])




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
dictionary.save('../data/TEST.dict')


corpus = [dictionary.doc2bow(text) for text in RAW_TEXTS]
corpora.MmCorpus.serialize('../data/testcorpus.mm', corpus)

