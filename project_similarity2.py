from collections import defaultdict
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist


if __name__ == '__main__':
    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    res = db.datasets.find({}, {"_id": 0, "identifier": 1, "description_ngram_np": 1})

    kw_vec = pd.DataFrame.from_pickle('keyword_vec_repr.pkl')

    # collect project vectors
    print "Collecting project vectors"
    projects = {r["identifier"]: kw_vec.ix[r["description_ngram_np"]] for r in res}

    proj_keys = projects.keys()
    similarities = defaultdict(list)
    print 'Calculating similarities'
    for i, p1 in enumerate(proj_keys):
        if i > 10:
            break

        print p1

        psims = dict()
        if i < len(proj_keys) - 1:
            for p2 in proj_keys[i + 1:]:
                # cdf = pd.DataFrame(1. - cdist(projects[p1], projects[p2], 'cosine'),
                #                    index=projects[p1].index,
                #                    columns=projects[p2].index)
                cdf = 1. - cdist(projects[p1], projects[p2], 'cosine')
                sim = np.mean((cdf.max(axis=0).mean(), cdf.max(axis=1).mean()))
                if not np.isnan(sim):
                    psims[p2] = sim

        psims = sorted(psims.items(), key=lambda s: s[1], reverse=True)
        if len(psims) > 10:
            psims = psims[:10]

        similarities[p1].append(psims)
        for p in psims:
            similarities[p[0]].append((p1, p[1]))

    # # keys = sorted(keywords.keys())
    # keys = keywords.keys()
    #
    # # calculate cosine similarity
    # print 'Calculating similarities'
    # similarity = 1. - squareform(pdist(np.array(keywords.values()), 'cosine'))
    # similarity = pd.DataFrame(1. - squareform(pdist(np.array(keywords.values()), 'cosine')), index=keys, columns=keys)
    #
    # keys = sorted(keys)
    #
    # # sort index/columns
    # similarity = similarity[keys].ix[keys]
    #
    # similarity.fillna(0.0, inplace=True)
    #
    # similarity.to_pickle('keyword_vector_cos_similarity.pkl')


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