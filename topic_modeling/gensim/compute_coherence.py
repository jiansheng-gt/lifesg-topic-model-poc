from multiprocessing import freeze_support
import matplotlib.pyplot as plt
import os
import pickle
from gensim import corpora, models

OUTPUT_DIR = 'output'
TOPICS_MIN = 2
TOPICS_MAX = 26
TOPICS_STEP = 1
RANDOM_STATE = 0 # for consistent benchmarking

if __name__ == "__main__":
    freeze_support()
    dictionary = corpora.Dictionary.load(os.path.join(OUTPUT_DIR, 'dictionary'))
    corpus = pickle.load(open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'rb'))
    texts = pickle.load(open(os.path.join(OUTPUT_DIR, 'texts-training.pkl'), 'rb'))

    cv_values = []
    umass_values = []
    topic_nums = range(TOPICS_MIN, TOPICS_MAX + 1, TOPICS_STEP)
    for num_topics in topic_nums:
        print('Calculating for num_topics:', num_topics)
        model = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics, passes=100, iterations=400, alpha='auto', eta='auto', eval_every=None, random_state=RANDOM_STATE)

        cv_model = models.CoherenceModel(model=model, texts=texts, topn=25, coherence='c_v')
        cv_value = cv_model.get_coherence()
        cv_values.append(cv_value)

        umass_model = models.CoherenceModel(model=model, texts=texts, topn=25, coherence='u_mass')
        umass_value = umass_model.get_coherence()
        umass_values.append(umass_value)
        print('c_v:', cv_value, ', umass:', umass_value)

    # Show graph
    x = topic_nums
    fig, ax = plt.subplots()
    twin1 = ax.twinx()

    p1, = ax.plot(x, cv_values, "b-")
    p2, = twin1.plot(x, umass_values, "r-")

    ax.set_xlabel("Num Topics")

    ax.set_ylabel("c_v")
    ax.yaxis.label.set_color(p1.get_color())
    ax.tick_params(axis='y', colors=p1.get_color())

    twin1.set_ylabel("U Mass")
    twin1.yaxis.label.set_color(p2.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())

    plt.savefig(os.path.join(OUTPUT_DIR, 'coherence.png'))
    print('Result saved')
