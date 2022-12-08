import json
import logging
import os
import sys
from typing import Literal, TypedDict

sys.path.append(os.getcwd())

import numpy as np
from sentence_transformers import SentenceTransformer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# all-MiniLM-L6-v2 vs all-mpnet-base-v2
# all-mpnet-base-v2 is more accurate
#
# Speed on full guide data:
# all-MiniLM-L6-v2 - 42 seconds
# all-mpnet-base-v2 - 2 min 22 seconds
model = SentenceTransformer('all-mpnet-base-v2')

DATA_DIR = 'data'
CHUNK_SIZE = 500
model.max_seq_length = 512

logging.info('Reading data...')
JsonInput = list[TypedDict(
	'JsonInput',
	{
		'contentType': str,
		'itemId': str,
		'text': str,
		'title': str
	}
)]

with open(os.path.join(DATA_DIR, 'scraper-results.json'), 'r') as f:
	documents: JsonInput = json.load(f)


# doc_reader = DataReader('data-with-external')
# documents = list(doc_reader)
# filenames = doc_reader.filenames

logging.info('Splitting texts into chunks...')
texts_chunked = []
for doc_num in range(len(documents)):
	doc_chunked = []
	doc_words = documents[doc_num]['text'].split()
	for i in range(0, len(doc_words), CHUNK_SIZE):
		doc_chunked.append(' '.join(doc_words[i:i + CHUNK_SIZE]))
	texts_chunked.append(doc_chunked)

logging.info('Calculating mean embeddings...')
embeddings = []
for text_chunked in texts_chunked:
	chunk_sims = model.encode(text_chunked)
	encoding_mean = chunk_sims.mean(0)
	embeddings.append(encoding_mean)

logging.info('Saving embeddings to JSON...')
EmbOutput = list[TypedDict(
	'EmbOutput',
	{
		'contentType': str,
		'itemId': str,
		'title': str,
		'embedding': list[int]
	}
)]

Payload = TypedDict(
	'Payload',
	{
		'impressionMultiplier': int,
		'redshiftWeightage': int,
		'embeddings': EmbOutput
	}
)
JsonOutput = TypedDict(
	'JsonOutput',
	{
		'type': Literal['LEVEL_3'],
		'payload': Payload
	}
)
result: JsonOutput = {
	'type': 'LEVEL_3',
	'payload': {
		'impressionMultiplier': -0.2,
		'redshiftWeightage': 0.2,
		'embeddings': []
	}
}

for index, doc_info in enumerate(documents):
	embedding_arr = np.array(embeddings[index])
	result['payload']['embeddings'].append({
		'contentType': doc_info['contentType'],
		'itemId': doc_info['itemId'],
		'title': doc_info['title'],
		'embedding': embedding_arr.tolist()
	})

with open(os.path.join(DATA_DIR, 'embeddings.json'), 'w') as out_file:
	json.dump(result, out_file)
logging.info('Done!')
