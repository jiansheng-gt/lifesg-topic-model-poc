import os
import pickle
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim_models

OUTPUT_DIR = 'output'

document_names = open(os.path.join(OUTPUT_DIR, 'document_names.txt')).read().split('\n')
dictionary = corpora.Dictionary.load(os.path.join(OUTPUT_DIR, 'dictionary'))
corpus = pickle.load(open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'rb'))
lda = models.ldamodel.LdaModel.load(os.path.join(OUTPUT_DIR, 'model'))

lda_display = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)

pyLDAvis.save_html(lda_display, os.path.join(OUTPUT_DIR, 'visualisation.html'))

topics = lda.get_document_topics(corpus)
document_topics = ''
for index, name in enumerate(document_names):
	document_topics += 'Document: ' + name + '\n'
	for topic_id, perc in topics[index]:
		document_topics += 'Topic ' + str(topic_id) + ' [' + str(perc) + ']:\n'
		document_topics += str(lda.show_topic(topic_id)) + '\n'
	document_topics += '\n'

open(os.path.join(OUTPUT_DIR, 'document_topics.txt'), 'w').write(document_topics)