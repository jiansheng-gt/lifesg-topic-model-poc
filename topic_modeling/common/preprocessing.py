import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4') # for wordnet lemmatizer

import spacy

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict

# spacy nlp
parser = spacy.load('en_core_web_sm')
lemmatizer = parser.get_pipe("lemmatizer")

# stopwords, might want to extend
en_stop = stopwords.words('english')

def tokenize(text):
    tokens = []
    doc = parser(text)

    for token in doc:
        if token.is_space:
            continue
        if token.like_url:
            continue
        if token.is_alpha:
            # use spacy lemmatizer as well
            tokens.append(token.lemma_.lower())

            # uncomment this if using other lemmatizer
            # tokens.append(token.lower_)
    return tokens

def get_lemma(word):
    return WordNetLemmatizer().lemmatize(word)

def get_stem(word):
    return PorterStemmer().stem(word)

# TODO: WIP proper processing
def preprocess(documents):

    # tokenize
    texts = [tokenize(document) for document in documents]

    # remove single characters
    texts = [
        [token for token in text if len(token) > 1]
        for text in texts
    ]

    # bigrams?

    # stem - root of words
    # texts = [
    #     [get_stem(token) for token in text]
    #     for text in texts
    # ]

    # lemmatize - same meaning words
    # comment out if using spacy lemmatizer
    # texts = [
    #     [get_lemma(token) for token in text]
    #     for text in texts
    # ]

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
