import os
from flask import request, Flask
import pandas as pd
from sentence_transformers import util
import numpy as np

CSV_PATH = '../data/embeddings.csv'

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    embeddings = pd.read_csv(os.path.join(app.root_path, CSV_PATH))
    embeddings.embedding = embeddings.embedding.apply(lambda x: np.array(x.split()).astype(np.float64))

    # a simple page that says hello
    @app.route('/api/guide-recs', methods=['POST'])
    def guide_recs():
        # get user clicks (req body)
        # TODO: handle empty body
        data = request.get_json(silent=True)

        print(data)
        if not data:
            user_recs = []
            for index, row in embeddings.iterrows():
                user_recs.append({
                    'id': index,
                    'title': row.guide_name,
                    'url': row.url,
                    'sim': 0
                })
            return user_recs

        # 1 click = 1 embedding
        user_embeddings = []
        for guide_id, clicks in data.items():
            for i in range(clicks):
                user_embeddings.append(embeddings.loc[int(guide_id)].embedding)

        user_embeddings_mean = np.array(user_embeddings).mean(0)

        user_recs = []
        # calculate cos sim
        for index, row in embeddings.iterrows():
            sim = util.cos_sim([user_embeddings_mean], [row.embedding])

            user_recs.append({
                'id': index,
                'title': row.guide_name,
                'url': row.url,
                'sim': sim[0][0].item()
            })

        sorted_recs = sorted(user_recs, key = lambda x: x['sim'], reverse=True)
        return sorted_recs

    return app