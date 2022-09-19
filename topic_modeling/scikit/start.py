import os
import sys
import pickle
sys.path.append(os.getcwd())

from topic_modeling.common.data_reader import DataReader

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

OUTPUT_DIR = 'output'

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

documents = DataReader('data')

no_features = 1000

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
# Pre-processing is done within CountVectorizer
print('Creating vectorizer...');
tf_vectorizer = CountVectorizer(
    max_df=0.95, 
    min_df=2, 
    stop_words='english', 
    token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")


print('Creating document term matrix...');
tf = tf_vectorizer.fit_transform(documents)
print("Getting feature names/..")
tf_feature_names = tf_vectorizer.get_feature_names_out()

no_topics = 10

print('Running LDA model...');
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

print('COMPELTED!');
no_top_words = 10
display_topics(lda, tf_feature_names, no_top_words)


with open('sklearn_model.pkl', 'wb') as fout:
    pickle.dump((tf_vectorizer, tf, lda), fout)
