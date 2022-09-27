import json
import logging
import os
import sys
sys.path.append(os.getcwd())

from topic_modeling.common.data_reader import DataReader
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# all-MiniLM-L6-v2 vs all-mpnet-base-v2
# all-mpnet-base-v2 is more accurate
#
# Speed on full guide data:
# all-MiniLM-L6-v2 - 42 seconds
# all-mpnet-base-v2 - 2 min 22 seconds
model = SentenceTransformer('all-mpnet-base-v2')

GUIDE_DATA = [
    ["Having A Baby", "https://www.life.gov.sg/guides/having-a-baby"],
    ["Enrolling In Preschool", "https://www.life.gov.sg/guides/enrolling-in-preschool"],
    ["Buy Hdb", "https://services.life.gov.sg/government-services/buy-hdb/"],
    ["Retrenchment Benefits And Measures", "https://www.life.gov.sg/guides/retrenchment-benefits-and-measures"],
    ["Support For Your Job Search", "https://www.life.gov.sg/guides/support-for-your-job-search"],
    ["Stay Healthy", "https://services.life.gov.sg/government-services/stay-healthy/"],
    ["Finances - Health Expenses", "https://services.life.gov.sg/government-services/finances/health-expenses/"],
    ["Finances - Family", "https://services.life.gov.sg/government-services/finances/family/"],
    ["Funding Your Retirement", "https://www.life.gov.sg/guides/funding-your-retirement"],
    ["Active Ageing", "https://www.life.gov.sg/guides/active-ageing"],
    ["Healthcare Financial Assistance", "https://www.life.gov.sg/guides/healthcare-financial-assistance"],
    ["Financial Assistance", "https://www.life.gov.sg/guides/financial-assistance"],
    ["Life After Heart Attack", "https://www.life.gov.sg/guides/life-after-heart-attack"],
    ["Education Career Opportunities", "https://www.life.gov.sg/guides/education-career-opportunities"],
    ["Senior Care Services", "https://www.life.gov.sg/guides/senior-care-services"],
    ["Resolving Employment Disputes", "https://www.life.gov.sg/guides/resolving-employment-disputes"],
    ["Becoming A Caregiver", "https://www.life.gov.sg/guides/becoming-a-caregiver"],
    ["Caregiver Stress", "https://www.life.gov.sg/guides/caregiver-stress"],
    ["P1 Registration", "https://www.life.gov.sg/guides/p1-registration"],
    ["Domestic Helper", "https://www.life.gov.sg/guides/domestic-helper"],
    ["Confinement Nanny", "https://www.life.gov.sg/guides/confinement-nanny"],
    ["Bringing Newborn Home", "https://www.life.gov.sg/guides/bringing-newborn-home"],
]
OUTPUT_DIR = 'output'
CHUNK_SIZE = 500
model.max_seq_length = 512

def get_guide_data(document_name):
    guide_num = int(document_name.split()[1].split('.')[0])
    data = GUIDE_DATA[guide_num - 1]
    return data[0], data[1]

logging.info('Reading data...')
doc_reader = DataReader('data-with-external')
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

logging.info('Saving embeddings to CSV...')
header = ['guide_name', 'url', 'filename', 'embedding']
df = pd.DataFrame(columns=header)
for index, filename in enumerate(filenames):
    guide_name, url = get_guide_data(filename)
    embedding_arr = np.array(embeddings[index])
    df.loc[index] = [
        guide_name,
        url,
        filename,
        ' '.join([str(item) for item in embedding_arr])
    ]

df.to_csv(os.path.join(OUTPUT_DIR, 'embeddings.csv'))

logging.info('Caclculating cosine similarity...')
doc_sims = {}
similarities = util.cos_sim(embeddings, embeddings)
for index, name in enumerate(filenames):
    similarity = []
    curr_guide_name, *_ = get_guide_data(name)
    logging.info('calculating similarity for guide: ' + curr_guide_name)

    for comp_index, comp_name in enumerate(filenames):
        if index == comp_index:
                continue
        comp_guide_name, *_ = get_guide_data(comp_name)

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