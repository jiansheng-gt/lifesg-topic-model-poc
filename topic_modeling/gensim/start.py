import os
import pickle
import sys
sys.path.append(os.getcwd())

import logging
from gensim import corpora
from topic_modeling.common.data_reader import DataReader
from topic_modeling.common.preprocessing import preprocess

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

OUTPUT_DIR = 'output'

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

logging.info('Processing training data...')
documents = DataReader('data-training')
texts_training = preprocess(documents)
pickle.dump(texts_training, open(os.path.join(OUTPUT_DIR, 'texts-training.pkl'), 'wb'))

logging.info('Processing guide data...')
documents = DataReader('data')
document_names = documents.get_filenames()
pickle.dump(document_names, open(os.path.join(OUTPUT_DIR, 'document_names.pkl'), 'wb'))
texts = preprocess(documents)
pickle.dump(texts, open(os.path.join(OUTPUT_DIR, 'texts.pkl'), 'wb'))

logging.info('Creating dictionary...')
dictionary = corpora.Dictionary(texts_training)
dictionary.save(os.path.join(OUTPUT_DIR, 'dictionary'))

logging.info('Creating BOW...')
corpus = [dictionary.doc2bow(text) for text in texts_training] # bag of words
pickle.dump(corpus, open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'wb'))

logging.info('Done!')