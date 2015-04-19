from collections import defaultdict
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist
from joblib import Parallel, delayed


def calc_sim(proj_keys, p1, i):
    print p1
    psims = dict()
    for p2 in proj_keys[i + 1:]:
        cdf = 1. - cdist(projects[p1], projects[p2], 'cosine')
        sim = np.mean((cdf.max(axis=0).mean(), cdf.max(axis=1).mean()))
        if not np.isnan(sim):
            psims[p2] = sim
    psims = sorted(psims.items(), key=lambda s: s[1], reverse=True)
    if len(psims) > 10:
        psims = psims[:10]
    s = defaultdict(list)
    s[p1].append(psims)
    for p in psims:
        s[p[0]].append((p1, p[1]))

    return s

if __name__ == '__main__':
    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    res = db.datasets.find({}, {"_id": 0, "identifier": 1, "description_ngram_np": 1})

    kw_vec = pd.read_pickle('keyword_vec_repr.pkl')

    # collect project vectors
    print "Collecting project vectors"
    projects = {r["identifier"]: kw_vec.ix[r["description_ngram_np"]] for r in res}

    # filter projects without keywords
    projects = {k: v for k, v in projects.iteritems() if len(v)}

    proj_keys = projects.keys()
    similarities = defaultdict(list)
    print 'Calculating similarities'
    # for i, p1 in enumerate(proj_keys):
    #     if i > 10:
    #         break
    #
    #     if i >= len(proj_keys) - 1:
    #         break
    #
    #     sims = calc_sim(proj_keys, p1, i)
    #
    #     for p, s in sims.iteritems():
    #         similarities[p].append(s)

    sims = Parallel(n_jobs=-1, verbose=7)(delayed(calc_sim)(proj_keys, p1, i) for i, p1 in enumerate(proj_keys[:-1]))