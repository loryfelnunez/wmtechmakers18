from gensim import corpora, models, similarities
import os


dictionary = corpora.Dictionary.load('../data/TEST.dict')
corpus = corpora.MmCorpus('../data/testcorpus.mm')


tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]


index = similarities.MatrixSimilarity(corpus_tfidf)

doc = """Socrates (/ˈsɒkrətiːz/;[2] Greek: Σωκράτης [sɔːkrátɛːs], Sōkrátēs; c. 470 – 399 BC)[3][4] 
was a classical Greek (Athenian) philosopher credited as one of the founders of Western philosophy, and 
as being the first moral philosopher,[5][6] of the western ethical tradition of thought.[7][8][9] An enigmatic 
figure, he made no writings, and is known chiefly through the accounts of classical writers writing after his lifetime, 
particularly his students Plato and Xenophon. Other sources include the contemporaneous Antisthenes, Aristippus, 
and Aeschines of Sphettos. Aristophanes, a playwright, is the only source to have written during his lifetime.[10][11]

Plato's dialogues are among the most comprehensive accounts of Socrates to survive from antiquity,
 though it is unclear the degree to which Socrates himself is "hidden behind his 'best disciple'.[12] 
 Through his portrayal in Plato's dialogues, Socrates has become renowned for his contribution to the 
 field of ethics, and it is this Platonic Socrates who lends his name to the concepts of Socratic irony and the 
 Socratic method, or elenchus.

The elenchus remains a commonly used tool in a wide range of discussions, and is a type of pedagogy 
in which a series of questions is asked not only to draw individual answers, but also to encourage 
fundamental insight into the issue at hand. Plato's Socrates also made important and lasting contributions to 
the field of epistemology, and his ideologies and approach have proven a strong foundation for much Western 
philosophy that has followed."""


vec_bow = dictionary.doc2bow(doc.lower().split())
vec_tfidf = tfidf[vec_bow]

import json
OUTPUT_PANTHEON = '../data/for_test.json'
DOCS = {}
with open(OUTPUT_PANTHEON, 'r+') as orgfile:
    json_data = json.load(orgfile)
    counter = 0
    for key, val in json_data.items():
        plain_text = val.get('plain_txt')
        DOCS[counter] = plain_text
        counter += 1


from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim import corpora, models, similarities
index_tmpfile = get_tmpfile("index")
index_all = similarities.Similarity(index_tmpfile, corpus_tfidf, num_features=len(dictionary))

for similarities in index:
    print ("START ======== ")
    sims = sorted(enumerate(similarities), key=lambda item: -item[1])
    for sim in sims:
        print('SCORE ', sim[1], ' ==> ', DOCS.get(sim[0])[0:140])





