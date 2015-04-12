from __future__ import unicode_literals
import json
from pymongo import MongoClient
from collections import Counter, defaultdict


client = MongoClient('proximus.modulusmongo.net:27017')
client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
db = client.tepO9seb

if __name__ == '__main__':
    counts = defaultdict(Counter)
    collocs = defaultdict(lambda: defaultdict(set))

    for i, kwds in enumerate(db.datasets.find({}, {'_id': 0, 'description_ngram_np': 1, 'source': 1})):
        if i and i % 1000 == 0:
            print i

        counts[kwds['source']].update(kwds['description_ngram_np'])

        for kw in kwds['description_ngram_np']:
            collocs[kwds['source']][kw] |= set(kwds['description_ngram_np']) - {kw}

    # collocs = dict(sorted(collocs.items(), key=lambda c: len(c)))

    collocs = {k: sorted([(v1, list(v2)) for v1, v2 in v.items()], key=lambda v_: len(v_[1]), reverse=True)
               for k, v in collocs.iteritems()}

    json.dump(counts, open('kw_counts.json', 'w'))
    json.dump(collocs, open('kw_collocations.json', 'w'))

    print 'Done'