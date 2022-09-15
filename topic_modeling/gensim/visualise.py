import os
import pickle
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim_models

OUTPUT_DIR = 'output'

dictionary = corpora.Dictionary.load(os.path.join(OUTPUT_DIR, 'dictionary'))
corpus = pickle.load(open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'rb'))
lda = models.ldamodel.LdaModel.load(os.path.join(OUTPUT_DIR, 'model'))

lda_display = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)

pyLDAvis.save_html(lda_display, os.path.join(OUTPUT_DIR, 'visualisation.html'))
