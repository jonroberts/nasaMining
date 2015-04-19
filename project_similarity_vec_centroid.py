from collections import defaultdict
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist
import pymongo


# def calc_sim(proj_keys, p1, i):
#     print p1
#     psims = dict()
#     for p2 in proj_keys[i + 1:]:
#         cdf = 1. - cdist(projects[p1], projects[p2], 'cosine')
#         sim = np.mean((cdf.max(axis=0).mean(), cdf.max(axis=1).mean()))
#         if not np.isnan(sim):
#             psims[p2] = sim
#     psims = sorted(psims.items(), key=lambda s: s[1], reverse=True)
#     if len(psims) > 10:
#         psims = psims[:10]
#     s = defaultdict(list)
#     s[p1].append(psims)
#     for p in psims:
#         s[p[0]].append((p1, p[1]))
#
#     return s

if __name__ == '__main__':
    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    res = db.datasets.find({}, {"_id": 0, "identifier": 1, "landingPage": 1, "description_ngram_np": 1})

    kw_vec = pd.read_pickle('keyword_vec_repr.pkl')

    # collect project vectors
    print "Collecting project vectors"
    projects = dict()
    # project_urls = dict()

    for r in res:
        projects[r['identifier']] = kw_vec.ix[r["description_ngram_np"]]
        # project_urls[r['identifier']] = r.get('landingPage', None)

    # projects = {r["identifier"]: kw_vec.ix[r["description_ngram_np"]] for r in res}

    # filter projects without keywords
    projects = {k: v for k, v in projects.iteritems() if len(v)}

    # take the centroid of each embedding dimension
    centroids = np.row_stack([np.mean(v) for v in projects.values()])

    dist = squareform(pdist(centroids, 'cosine'))
    sim_df = pd.DataFrame(1. - dist, index=projects.keys(), columns=projects.keys())
    sim_df.fillna(0.0, inplace=True)

    sim_df.to_pickle('keyword_vec_centroid_sims.pkl')

    recs = []
    for i, sims in sim_df.iterrows():
        r = sims.sort(inplace=False, ascending=False).head(25)
        recs += [{'identifier': i, 'rec': ri, 'sim': rs} for ri, rs in r.to_dict().items() if ri != i]

    db.related_datasets.insert(recs)
    db.related_datasets.create_index('identifier', background=True)
    db.related_datasets.create_index([('identifier', pymongo.ASCENDING), ('sim', pymongo.DESCENDING)])