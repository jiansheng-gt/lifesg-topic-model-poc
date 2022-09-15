from multiprocessing import freeze_support
import matplotlib.pyplot as plt
import os
import pickle
from gensim import corpora, models

OUTPUT_DIR = 'output'
TOPICS_MIN = 4
TOPICS_MAX = 10
TOPICS_STEP = 1
RANDOM_STATE = 123 # for consistent benchmarking


if __name__ == "__main__":
    freeze_support()
    document_names = open(os.path.join(OUTPUT_DIR, 'document_names.txt')).read().split('\n')
    dictionary = corpora.Dictionary.load(os.path.join(OUTPUT_DIR, 'dictionary'))
    corpus = pickle.load(open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'rb'))
    texts_str = open(os.path.join(OUTPUT_DIR, 'tokens.txt')).read()
    texts = [
      [token for token in text.split()]
      for text in texts_str.split('\n')
    ]
    texts.pop() # newline at end of file

    coherence_values = []
    model_list = []
    for num_topics in range(TOPICS_MIN, TOPICS_MAX, TOPICS_STEP):
        print('Calculating for num_topics:', num_topics)
        model = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics, passes=15, iterations=200, random_state=RANDOM_STATE)
        model_list.append(model)
        coherencemodel = models.CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence = coherencemodel.get_coherence()
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
