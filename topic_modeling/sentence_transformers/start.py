import json
import logging
import os
import sys
sys.path.append(os.getcwd())

from topic_modeling.common.data_reader import DataReader
from sentence_transformers import SentenceTransformer, util

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# all-MiniLM-L6-v2 vs all-mpnet-base-v2
# all-mpnet-base-v2 is more accurate
#
# Speed on full guide data:
# all-MiniLM-L6-v2 - 42 seconds
# all-mpnet-base-v2 - 2 min 22 seconds
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
CHUNK_SIZE = 500
model.max_seq_length = 512

def get_guide_name(document_name):
    guide_num = int(document_name.split()[1].split('.')[0])
    return GUIDE_URLS[guide_num - 1]

logging.info('Reading data...')
doc_reader = DataReader('data')
documents = list(doc_reader)
filenames = doc_reader.filenames

logging.info('Splitting texts into chunks...')
texts_chunked = []
for doc_num in range(len(documents)):
    doc_chunked = []
    doc_words = documents[doc_num].split()
    for i in range(0, len(doc_words), CHUNK_SIZE):
        doc_chunked.append(' '.join(doc_words[i:i + CHUNK_SIZE]))
    texts_chunked.append(doc_chunked)

logging.info('Calculating mean embeddings...')
embeddings = []
for text_chunked in texts_chunked:
    chunk_sims = model.encode(text_chunked)
    encoding_mean = chunk_sims.mean(0)
    embeddings.append(encoding_mean)

logging.info('Caclculating cosine similarity...')
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

        # Filter if needed
        # if sim > 0.5:
        similarity.append(tuple([comp_guide_name, sim.item()]))

    # sort by highest similarity
    sorted_similar = sorted(similarity, key = lambda x: x[1], reverse=True)
    doc_sims[curr_guide_name] = tuple(sorted_similar)

result = json.dumps(doc_sims, indent = 4)
open(os.path.join(OUTPUT_DIR, 'doc_similarity.json'), 'w').write(result)
logging.info('Done!')