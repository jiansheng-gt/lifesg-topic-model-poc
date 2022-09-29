import pandas as pd
from surprise import Reader, Dataset, KNNWithMeans


data = {
    "item": [1, 5, 10, 3, 5, 10, 10, 1, 3, 5],
    "user": ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'D', 'D', 'D'],
}

read_data = {
    'A': [1, 5, 10],
    'B': [3, 5, 10],
    'C': [10],
    'D': [1, 3, 5],
    'E': [2]
}
users = ['A', 'B', 'C', 'D', 'E']
items = [1, 2, 3, 5, 10]


data = []
for user in users:
    for item in items:
        # read = 0
        if item in read_data[user]:
            read = 1
            data.append([user, item, read])
# load data in pandas
df = pd.DataFrame(data)
print(df)

reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df, reader)

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}
algo = KNNWithMeans(sim_options=sim_options)
trainingSet = data.build_full_trainset()
algo.fit(trainingSet)
prediction = algo.predict('C', 2)
print(prediction)
