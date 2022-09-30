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

    # 1 click = 1 embedding
    user_embeddings = []
    for guide_id, clicks in user_clicks.items():
        for i in range(clicks):
            user_embeddings.append(embeddings.loc[int(guide_id)].embedding)

    user_embeddings_mean = np.array(user_embeddings).mean(0)

    user_recs = pd.DataFrame([], columns=rec_cols)
    # calculate cos sim
    for index, row in embeddings.iterrows():
        sim = util.cos_sim([user_embeddings_mean], [row.embedding])

        user_recs.loc[index] = {
            'id': index,
            'title': row.guide_name,
            'url': row.url,
            'sim': sim[0][0].item()
        }

    sorted_recs = user_recs.sort_values(by=['sim'], ascending=False)
    return sorted_recs
