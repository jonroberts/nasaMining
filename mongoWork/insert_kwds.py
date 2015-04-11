from pymongo import MongoClient
import json

client = MongoClient('proximus.modulusmongo.net:27017')
client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
db = client.tepO9seb

if __name__ == '__main__':
    data = json.load(open('data/nasa_kw.json'))['dataset']

    for i, d in enumerate(data):
        if i and i % 100 == 0:
            print i

        db.datasets.update({'identifier': d['identifier']}, {'$set': {
            'description_bigram_kw': d['description_bigram_kw'],
            'description_textrank_kw': d['description_textrank_kw']
        }})