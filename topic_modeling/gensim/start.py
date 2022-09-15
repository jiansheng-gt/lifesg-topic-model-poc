import os
import pickle
import sys
sys.path.append(os.getcwd())

import pprint
import logging
from gensim import corpora, models
from topic_modeling.common.data_reader import DataReader
from topic_modeling.common.preprocessing import preprocess

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

OUTPUT_DIR = 'output'

logging.info('Reading data...');
documents = DataReader('data')
filenames = documents.get_filenames()
open(os.path.join(OUTPUT_DIR, 'document_names.txt'), 'w').write('\n'.join(filenames))
logging.info('Reading data DONE');

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

logging.info('Processing documents...');
texts = preprocess(documents)

text_str = '';
for text in texts:
	text_str += ' '.join(text) + '\n'
open(os.path.join(OUTPUT_DIR, 'tokens.txt'), 'w').write(text_str)
logging.info('Processing documents DONE');

logging.info('Creating dictionary...');
dictionary = corpora.Dictionary(texts)
dictionary.save(os.path.join(OUTPUT_DIR, 'dictionary'))

logging.info('Creating BOW...');
corpus = [dictionary.doc2bow(text) for text in texts] # bag of words
pickle.dump(corpus, open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'wb'))

logging.info('Running LDA model...');
model = models.LdaModel(corpus, id2word=dictionary, num_topics=5, passes=15, iterations=200)
model.save(os.path.join(OUTPUT_DIR, 'model'))

logging.info('COMPELTED!');
pprint.pprint(model.print_topics())
