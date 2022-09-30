import pandas as pd
from scipy.spatial.distance import cosine

read_data = {
    'A': [1, 2, 5],
    'B': [3, 5, 2],
    'C': [1, 4],
    'D': [1, 3, 5],
    'E': [2]
}
users = ['A', 'B', 'C', 'D', 'E']
items = [1, 2, 3, 4, 5]

data = [[0 for col in range(len(items) + 1)] for row in range(len(users))]

# load data in pandas
df = pd.DataFrame(
    data, columns=['user', 'guide 1', 'guide 2', 'guide 3', 'guide 4', 'guide 5'])

df['user'] = users
for index, user in enumerate(read_data):
    for item in read_data[user]:
        df.iat[index, item] = 1

print(df)

# drop user column
df = df.drop('user', axis=1)

# Create a placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=df.columns, columns=df.columns)


# Lets fill in those empty spaces with cosine similarities
# Loop through the columns
for i in range(0, len(data_ibs.columns)):
    # Loop through the columns for each column
    for j in range(0, len(data_ibs.columns)):
        # Fill in placeholder with cosine similarities
        data_ibs.iloc[i, j] = 1 - cosine(df.iloc[:, i], df.iloc[:, j])

print(data_ibs)

# Create a placeholder items for closest neighbours to an item
data_neighbours = pd.DataFrame(index=data_ibs.columns, columns=range(1, 6))

# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0, len(data_ibs.columns)):
    data_neighbours.iloc[i] = data_ibs.iloc[0:,
                                            i].sort_values(ascending=False).index

print(data_neighbours.iloc[:, 1:])
