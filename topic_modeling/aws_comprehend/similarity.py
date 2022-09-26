import logging
import os
import sys
import json

sys.path.append(os.getcwd())
import pandas as pd
import numpy as np
from gensim import matutils

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

OUTPUT_DIR = 'output'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

doc_topics = pd.read_csv('aws-data/output-13topics-full/doc-topics.csv')
topic_terms = pd.read_csv('aws-data/output-13topics-full/topic-terms.csv')
NUM_DOCS = len(doc_topics['docname'].unique())
NUM_TOPICS = len(topic_terms['topic'].unique())

doc_topic_dist = np.empty(NUM_DOCS, dtype=object)
for doc_index in range(len(doc_topic_dist)):
    doc_topic_dist[doc_index] = []
    for topic_index in range(NUM_TOPICS):
        doc_topic_dist[doc_index].append(tuple([topic_index, 0]))


for index in range(len(doc_topics)):
    docname, topic, proportion = doc_topics.iloc[index]
    guide_num = int(docname.split()[1].split('.')[0])
    doc_topic_dist[guide_num - 1][topic] = tuple([topic, proportion])


doc_sims = {}
sim_cache = {}
for index in range(NUM_DOCS):
    similarity = []
    curr_guide_name = GUIDE_URLS[index]
    logging.info('calculating similarity for guide: ' + curr_guide_name)

    curr_doc = doc_topic_dist[index]

    for comp_index in range(NUM_DOCS):
        if index == comp_index:
            continue

        comp_guide_name = GUIDE_URLS[comp_index]

        sim = 0
        if str(index) + ',' + str(comp_index) in sim_cache:
            sim = sim_cache[str(index) + ',' + str(comp_index)]
        else:
            comp_doc = doc_topic_dist[comp_index]
            sim = matutils.cossim(curr_doc, comp_doc)
            sim_cache[str(index) + ',' + str(comp_index)] = sim
            sim_cache[str(comp_index) + ',' + str(index)] = sim

        if sim > 0.5:
            similarity.append(tuple([comp_guide_name, sim]))

    # sort by highest similarity
    sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
    doc_sims[curr_guide_name] = tuple(sorted_similar)

result = json.dumps(doc_sims, indent = 4)
open(os.path.join(OUTPUT_DIR, f'doc_similarity_aws_{NUM_TOPICS}.json'), 'w').write(result)
