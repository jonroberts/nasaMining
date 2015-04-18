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

    # keys = sorted(keywords.keys())
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


    # similarity = pd.DataFrame(index=keys, columns=keys)
    #
    # print 'Calculating similarities'
    #
    # for i, ki in enumerate(keys):
    #     print i
    #     similarity.iloc[i, i + 1:] = [keywords[ki].dot(keywords[kj]) for kj in keys[i + 1:]]
    #
    # print 'done'
    #
    # similarity.to_pickle('keyword_vector_similarity.pkl')

    # for i, pair in enumerate(combinations(keywords, 2)):
    #     if i > 0 and i % 1000 == 0:
    #         print i
    #
    #     if i > 1000000:
    #         break
    #
    #     key = sorted(pair, key=unicode.lower)
    #
    #     similarity.loc[key[0], key[1]] = keywords[key[0]].dot(keywords[key[1]])
        # similarity[key[0]][key[1]] = keywords[key[0]].dot(keywords[key[1]])
        # similarity.append({'keyword': key, 'similarity': float(keywords[key[0]].dot(keywords[key[1]]))})

    # with open('data/keyword_vector_similarity.json', 'w') as f:
    #     json.dump(similarity, f)