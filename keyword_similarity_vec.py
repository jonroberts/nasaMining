from pymongo import MongoClient
from spacy.en import English
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform


if __name__ == '__main__':
    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    res = db.datasets.find({}, {"_id": 0, "description_ngram_np": 1})

    nlp = English()

    # get all unique keywords and their (additive) vector representation
    print 'Vectorizing unique keywords'
    keywords = dict()
    for r in res:
        for kw in r["description_ngram_np"]:
            keywords[kw] = sum([token.repvec for token in nlp(kw)])

    kw_vec = pd.DataFrame.from_dict(keywords).T
    kw_vec.to_pickle('keyword_vec_repr.pkl')

    keys = keywords.keys()

    # calculate cosine similarity
    print 'Calculating similarities'
    similarity = 1. - squareform(pdist(np.array(keywords.values()), 'cosine'))
    similarity = pd.DataFrame(1. - squareform(pdist(np.array(keywords.values()), 'cosine')), index=keys, columns=keys)

    keys = sorted(keys)

    # sort index/columns
    similarity = similarity[keys].ix[keys]

    similarity.fillna(0.0, inplace=True)

    similarity.to_pickle('keyword_vector_cos_similarity.pkl')