import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4') # for wordnet lemmatizer

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict

# stopwords, might want to extend
en_stop = stopwords.words('english')
# en_stop = set('for a of the and to in'.split())

def tokenize(text):
    return text.lower().split()

def get_lemma(word):
    return WordNetLemmatizer().lemmatize(word)

# TODO: WIP proper processing
def preprocess(documents):

    # tokenize
    texts = [tokenize(document) for document in documents]

    # remove special characters

    # bigrams?

    # stem - root of words

    # lemmatize - same meaning words
    texts = [
        [get_lemma(token) for token in text]
        for text in texts
    ]

    # filter stop words
    texts = [
        [token for token in text if token not in en_stop]
        for text in texts
    ]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]

    return texts
