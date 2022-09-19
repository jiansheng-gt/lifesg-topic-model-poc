import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

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

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))

def get_guide_name(document_name):
    guide_num = int(document_name.split()[1].split('.')[0])
    return GUIDE_URLS[guide_num - 1]

OUTPUT_DIR = 'output'

document_names = open(os.path.join(OUTPUT_DIR, 'document_names.txt')).read().split('\n')

with open(os.path.join(OUTPUT_DIR, 'sklearn_model.pkl'), 'rb') as f:
    tf_vectorizer, tf, lda = pickle.load(f)

doc_topic_dist = lda.transform(tf)
doc_sims = {}
for index in range(len(doc_topic_dist)):
    similarity = []

    for comp_index in range(len(doc_topic_dist)):
        if index == comp_index:
            continue
        sim = cosine_similarity([doc_topic_dist[index]], [doc_topic_dist[comp_index]])
        similarity.append(tuple([GUIDE_URLS[comp_index], sim[0][0]]))

    sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
    # sort by highest similarity
    doc_sims[GUIDE_URLS[index]] = tuple(sorted_similar)


result = json.dumps(doc_sims, indent=4, default=default)

sim = cosine_similarity(doc_topic_dist)

open(os.path.join(OUTPUT_DIR, 'doc_similarity_sklearn.txt'), 'w').write(result)
