import json
import logging
import os
import sys
sys.path.append(os.getcwd())

from topic_modeling.common.data_reader import DataReader
from sentence_transformers import SentenceTransformer, util

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# all-MiniLM-L6-v2 not as accurate
model = SentenceTransformer('all-mpnet-base-v2')

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

def get_guide_name(document_name):
    guide_num = int(document_name.split()[1].split('.')[0])
    return GUIDE_URLS[guide_num - 1]

documents = DataReader('data')
texts = list(documents)
filenames = documents.filenames

embeddings = model.encode(texts)


doc_sims = {}
similarities = util.cos_sim(embeddings, embeddings)

for index, name in enumerate(filenames):
    similarity = []
    curr_guide_name = get_guide_name(name)
    logging.info('calculating similarity for guide: ' + curr_guide_name)

    for comp_index, comp_name in enumerate(filenames):
        if index == comp_index:
                continue
        comp_guide_name = get_guide_name(comp_name)

        sim = similarities[index][comp_index]

        if sim > 0.5:
            similarity.append(tuple([comp_guide_name, sim.item()]))

    # sort by highest similarity
    sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
    doc_sims[curr_guide_name] = tuple(sorted_similar)

result = json.dumps(doc_sims, indent = 4)
open(os.path.join(OUTPUT_DIR, 'doc_similarity.json'), 'w').write(result)