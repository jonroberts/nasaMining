import json
from pymongo import MongoClient

client = MongoClient('proximus.modulusmongo.net:27017')
client.tepO9seb.authenticate('nasahack', 'hacking4nasa')

db = client.tepO9seb

if __name__ == '__main__':
    counts = json.load(open('kw_counts.json'))

    nasa_kwds = counts['http://data.nasa.gov/data.json'].keys()

    others = set(counts.keys()) - {'http://data.nasa.gov/data.json'}

    total = 0

    all_kwds = set(nasa_kwds)
    total_kwds = sum(counts['http://data.nasa.gov/data.json'].values())

    for other in others:
        print other
        res = db.datasets.find({
            'source': other,
            'description_ngram_np': {'$in': nasa_kwds}
        }).count()
        print res

        total += res

        all_kwds |= set(counts[other].keys())
        total_kwds += sum(counts[other].values())

    print 'Total:', total
    print 'Distinct keywords:', len(all_kwds)
    print 'Total keywords:', total_kwds