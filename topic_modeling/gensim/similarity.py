import logging
from multiprocessing import freeze_support
import os
import sys

sys.path.append(os.getcwd())
import pickle
from gensim import corpora, models, matutils
import json

from topic_modeling.common.data_reader import DataReader

GUIDE_URLS = [
    "/guides/having-a-baby",
    "/guides/enrolling-in-preschool",
    "/government-services/buy-hdb/",
    "/guides/retrenchment-benefits-and-measures",
    "/guides/support-for-your-job-search",
    "/government-services/stay-healthy/",
    "/government-services/finances/health-expenses/",
    "/government-services/finances/family/",
    "/guides/funding-your-retirement",
    "/guides/active-ageing",
    "/guides/healthcare-financial-assistance",
    "/guides/financial-assistance",
    "/guides/life-after-heart-attack",
    "/guides/education-career-opportunities",
    "/guides/senior-care-services",
    "/guides/resolving-employment-disputes",
    "/guides/becoming-a-caregiver",
    "/guides/caregiver-stress",
    "/guides/p1-registration",
    "/guides/domestic-helper",
    "/guides/confinement-nanny",
    "/guides/bringing-newborn-home",
];

def get_guide_name(document_name):
    guide_num = int(document_name.split()[1].split('.')[0])
    return GUIDE_URLS[guide_num - 1]

OUTPUT_DIR = 'output'
NUM_TOPICS = 13
COHERENCE_MEASURE = 'c_v' # either c_v or u_mass

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

dictionary: corpora.Dictionary = corpora.Dictionary.load(os.path.join(OUTPUT_DIR, 'dictionary'))
texts_training = pickle.load(open(os.path.join(OUTPUT_DIR, 'texts-training.pkl'), 'rb'))
corpus = pickle.load(open(os.path.join(OUTPUT_DIR, 'corpus.pkl'), 'rb'))

if __name__ == "__main__":
    freeze_support()

    # iterate 10 times to get best coherence score
    lda: models.LdaModel = None
    best_score = float('-inf')
    for i in range(10):
        print('Iteration:', i)
        curr_lda = models.LdaModel(corpus, id2word=dictionary, num_topics=NUM_TOPICS, passes=100, iterations=400, alpha='auto', eta='auto', eval_every=None)

        curr_score = models.CoherenceModel(model=curr_lda, texts=texts_training, topn=25, coherence=COHERENCE_MEASURE).get_coherence()
        print('curr_score:', curr_score)

        if curr_score > best_score:
            lda = curr_lda
            best_score = curr_score
    print('highest score:', best_score)

    # Similarity for full guide data using best model
    full_texts = pickle.load(open(os.path.join(OUTPUT_DIR, 'texts.pkl'), 'rb'))
    full_texts_list = [dictionary.doc2bow(text) for text in full_texts]
    document_names = pickle.load(open(os.path.join(OUTPUT_DIR, 'document_names.pkl'), 'rb'))

    doc_sims = {}
    sim_cache = {}
    for index, name in enumerate(document_names):
        similarity = []
        curr_guide_name = get_guide_name(name)
        logging.info('calculating similarity for guide: ' + curr_guide_name)

        curr_doc = lda.get_document_topics(full_texts_list[index], minimum_probability=0)

        for comp_index, comp_name in enumerate(document_names):
            if index == comp_index:
                continue

            comp_guide_name = get_guide_name(comp_name)

            sim = 0
            if str(index) + ',' + str(comp_index) in sim_cache:
                sim = sim_cache[str(index) + ',' + str(comp_index)]
            else:
                comp_doc = lda.get_document_topics(full_texts_list[comp_index], minimum_probability=0)
                sim = matutils.cossim(curr_doc, comp_doc)
                sim_cache[str(index) + ',' + str(comp_index)] = sim
                sim_cache[str(comp_index) + ',' + str(index)] = sim

            if sim > 0.5:
                similarity.append(tuple([comp_guide_name, sim]))

        # sort by highest similarity
        sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
        doc_sims[curr_guide_name] = tuple(sorted_similar)

    result = json.dumps(doc_sims, indent = 4)
    open(os.path.join(OUTPUT_DIR, 'doc_similarity.json'), 'w').write(result)
