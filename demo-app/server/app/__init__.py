import os

from app.recommend import get_recs
from flask import request, Flask
import pandas as pd
import numpy as np

CSV_PATH = '../data/embeddings.csv'

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    embeddings = pd.read_csv(os.path.join(app.root_path, CSV_PATH))
    embeddings.embedding = embeddings.embedding.apply(lambda x: np.array(x.split()).astype(np.float64))

    @app.route('/api/guide-recs', methods=['POST'])
    def guide_recs():
        # get user clicks (req body)
        data = request.get_json(silent=True)
        recs = get_recs(embeddings, data)
        return recs.to_dict('records')

    return app
