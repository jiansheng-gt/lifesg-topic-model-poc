import os
import pickle
import json
from gensim.matutils import hellinger

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

document_names = open(os.path.join(OUTPUT_DIR, 'document_names.txt')).read().split('\n')

with open(os.path.join(OUTPUT_DIR, 'sklearn_model.pkl'), 'rb') as f:
    tf_vectorizer, tf, lda = pickle.load(f)

doc_topic_dist = lda.transform(tf)
bag_of_words = []

for doc_index in range(len(doc_topic_dist)):
    bag_of_words.append([])
    for topic_index in range(len(doc_topic_dist[doc_index])):
        p = doc_topic_dist[doc_index][topic_index]
        bag_of_words[doc_index].append((topic_index, p))

doc_sims = {}
for index, name in enumerate(document_names):
    similarity = []

    curr_doc = bag_of_words[index]

    for comp_index, comp_name in enumerate(document_names):
        if index == comp_index:
            continue
        comp_doc = bag_of_words[comp_index]
        sim = hellinger(curr_doc, comp_doc)
        similarity.append(tuple([get_guide_name(comp_name), sim]))

    sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
    # sort by highest similarity
    doc_sims[get_guide_name(name)] = tuple(sorted_similar)

result = json.dumps(doc_sims, indent = 4)

open(os.path.join(OUTPUT_DIR, 'doc_similarity_hellinger.txt'), 'w').write(result)