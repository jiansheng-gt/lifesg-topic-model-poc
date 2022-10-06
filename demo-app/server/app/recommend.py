import pandas as pd
import numpy as np
from sentence_transformers import util

rec_cols = ['id', 'title', 'url', 'sim']

def get_recs(embeddings: pd.DataFrame, user_clicks):
    if not user_clicks:
        user_recs = pd.DataFrame([], columns=rec_cols)
        # randomize
        for index, row in embeddings.sample(frac=1).iterrows():
            user_recs.loc[index] = [index, row.guide_name, row.url, 0]
        return user_recs


    # user embeddings - dot product of user interests with guide embeddings
    user_ratings = pd.DataFrame(np.zeros((len(embeddings), 1)), columns=['rating'])
    for guide_id, clicks in user_clicks.items():
      user_ratings.at[int(guide_id), 'rating'] = clicks

    guide_embeddings = embeddings.loc[:, 'embedding'].to_numpy()
    user_embeddings = guide_embeddings.dot(user_ratings)[0]

    user_recs = pd.DataFrame([], columns=rec_cols)
    # calculate cos sim
    for index, row in embeddings.iterrows():
        sim = util.cos_sim([user_embeddings], [row.embedding])

        user_recs.loc[index] = {
            'id': index,
            'title': row.guide_name,
            'url': row.url,
            'sim': sim[0][0].item()
        }

    sorted_recs = user_recs.sort_values(by=['sim'], ascending=False)
    return sorted_recs
