import os
import sys
sys.path.append(os.getcwd())

import pprint
import logging
from gensim import corpora, models
from topic_modeling.common.data_reader import DataReader
from topic_modeling.common.preprocessing import preprocess

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = DataReader('data')

# documents = [
#     "Human machine interface for lab abc computer applications",
#     "A survey of user opinion of computer system response time",
#     "The EPS user interface management system",
#     "System and human system engineering testing of EPS",
#     "Relation of user perceived response time to error measurement",
#     "The generation of random binary unordered trees",
#     "The intersection graph of paths in trees",
#     "Graph minors IV Widths of trees and well quasi ordering",
#     "Graph minors A survey",
# ]

texts = preprocess(documents)

dictionary = corpora.Dictionary(texts)

pprint.pprint(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts] # bag of words

model = models.LdaModel(corpus, id2word=dictionary, num_topics=2)

pprint.pprint(model)