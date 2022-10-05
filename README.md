# Setup

1. Install virtualenv

```
pip3 install virtualenv
```

2. Create virtual environment

```
virtualenv venv
```

3. Activate the virtual environment

```
source venv/bin/activate
```

4. Install dependencies

```
pip3 install -r requirements.txt
```

# Gensim

1. Create dictionary and Bag of Words

```
python topic_modeling/gensim/start.py
```

2. Calculate coherence for varying number of topics

```
python topic_modeling/gensim/compute_coherence.py
```

3. Compute similarity between guides

```
python topic_modeling/gensim/similarity.py
```

4. Visualisation of topics (**a model needs to be saved first**)

```
python topic_modeling/gensim/visualise.py
```

# Sentence Transformers

1. Run Sentence Transformers

```
python topic_modeling/sentence_transformers/start.py
```
