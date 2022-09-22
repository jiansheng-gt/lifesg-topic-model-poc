import os
import sys
import pickle
sys.path.append(os.getcwd())
import numpy as np
from multiprocessing import freeze_support
import matplotlib.pyplot as plt

from preprocess import preprocess, sent_to_words
from topic_modeling.common.data_reader import DataReader

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
from tmtoolkit.topicmod.evaluate import metric_coherence_gensim

OUTPUT_DIR = 'output'

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

# online sample dataset
# dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
# documents = dataset.data

documents = DataReader('data')

# preprocess documents
preprocessed_documents = preprocess(documents)

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
tf = tf_vectorizer.fit_transform(preprocessed_documents)
print("Getting feature names/..")
tf_feature_names = tf_vectorizer.get_feature_names_out()

no_topics = 10

print('Running LDA model...');
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=15, max_doc_update_iter=200).fit(tf)

print('COMPELTED!');
no_top_words = 10
display_topics(lda, tf_feature_names, no_top_words)

# Log Likelyhood: Higher the better
print("Log Likelihood: ", lda.score(tf))

# Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
print("Perplexity: ", lda.perplexity(tf))

# document topic distribution
# lda.transform(tf)

pickle.dump((tf_vectorizer, tf, lda), open(os.path.join(OUTPUT_DIR, 'sklearn_model.pkl'), 'wb'))

# Define Search Param
search_params = {'n_components': [5, 10, 15] }
# Include paramters to do grid search on 
# Note: More parameters means longer runtime, each run is done 5 times, set cv=n
# 'max_iter':(10,20,50)
# 'learning_decay': [.5, .7, .9]

# Init the Model
lda = LatentDirichletAllocation()

if __name__ == "__main__":
    freeze_support()
    def scorer(estimator, X,y=None):
        return metric_coherence_gensim(measure='c_v', 
                                    top_n=25, 
                                    topic_word_distrib=estimator.components_, 
                                    dtm=tf, 
                                    vocab=np.array(tf_vectorizer.get_feature_names_out()),
                                    texts=sent_to_words(documents),
                                    return_mean=True)

    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=search_params, scoring=scorer, verbose=10)

    # Do the Grid Search
    model.fit(tf)

    # Best Model
    best_lda_model = model.best_estimator_

    # Model Parameters
    print("Best Model's Params: ", model.best_params_)

    # Log Likelihood Score
    print("Best Log Likelihood Score: ", model.best_score_)

    # Perplexity
    print("Model Perplexity: ", best_lda_model.perplexity(tf))


    # Get Log Likelyhoods from Grid Search Output
    n_topics = [5, 10, 15]

    result = model.cv_results_
    print(model.cv_results_)

    log_likelyhoods_5 = [round(result['mean_test_score'][index]) for index in range(len(result['params'])) if result['params'][index]['learning_decay']==0.5]
    log_likelyhoods_7 = [round(result['mean_test_score'][index]) for index in range(len(result['params'])) if result['params'][index]['learning_decay']==0.7]
    log_likelyhoods_9 = [round(result['mean_test_score'][index]) for index in range(len(result['params'])) if result['params'][index]['learning_decay']==0.9]

    # Show graph
    plt.figure(figsize=(12, 8))
    plt.plot(n_topics, log_likelyhoods_5, label='0.5')
    plt.plot(n_topics, log_likelyhoods_7, label='0.7')
    plt.plot(n_topics, log_likelyhoods_9, label='0.9')
    plt.title("Choosing Optimal LDA Model")
    plt.xlabel("Num Topics")
    plt.ylabel("Log Likelyhood Scores")
    plt.legend(title='Learning decay', loc='best')
    plt.show()
