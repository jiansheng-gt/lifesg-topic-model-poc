import matplotlib.pyplot as plt
import os
import sys
import pickle
import numpy as np
sys.path.append(os.getcwd())
from sklearn.decomposition import LatentDirichletAllocation


from tmtoolkit.topicmod.evaluate import metric_coherence_gensim
from topic_modeling.common.data_reader import DataReader

OUTPUT_DIR = 'output'
TOPICS_MIN = 5
TOPICS_MAX = 15
TOPICS_STEP = 1
RANDOM_STATE = 123 # for consistent benchmarking

documents = DataReader('data')

with open(os.path.join(OUTPUT_DIR, 'sklearn_model.pkl'), 'rb') as f:
    tf_vectorizer, tf, lda_file = pickle.load(f)

tokenizer = tf_vectorizer.build_tokenizer()
tokenized_texts = []
for text in documents: tokenized_texts.append(tokenizer(text.lower()))

if __name__ == "__main__":

    coherence_values = []
    model_list = []
    for num_topics in range(TOPICS_MIN, TOPICS_MAX, TOPICS_STEP):
        print('Calculating for num_topics:', num_topics)

        lda = LatentDirichletAllocation(
          n_components=num_topics, 
          max_iter=15, 
          max_doc_update_iter=200, 
          random_state=RANDOM_STATE).fit(tf)

        coherence = metric_coherence_gensim(measure='c_v', 
                                top_n=25, 
                                topic_word_distrib=lda.components_, 
                                dtm=tf, 
                                vocab=np.array(tf_vectorizer.get_feature_names_out()),
                                texts=tokenized_texts,
                                return_mean=True)

        coherence_values.append(coherence)
        print('Done! Result:', coherence)

    # Show graph
    limit=TOPICS_MAX; start=TOPICS_MIN; step=TOPICS_STEP;
    x = range(start, limit, step)

    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
