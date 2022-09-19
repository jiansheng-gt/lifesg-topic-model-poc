import os
import pickle
import pyLDAvis
import pyLDAvis.sklearn

OUTPUT_DIR = 'output'

with open(os.path.join(OUTPUT_DIR, 'sklearn_model.pkl'), 'rb') as f:
    tf_vectorizer, tf, lda = pickle.load(f)

lda_display = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)

pyLDAvis.save_html(lda_display, os.path.join(OUTPUT_DIR, 'sklearn_visualisation.html'))
