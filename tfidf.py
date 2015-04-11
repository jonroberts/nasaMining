from __future__ import unicode_literals
import json, operator
from itertools import combinations
from gensim.models.tfidfmodel import TfidfModel

if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']
    descs = []

    for i, ds in enumerate(dataset):
        descs.append(ds['description'])
    
    tfidf = TfidfModel(descs)
    print(tfidf['atmosphere'])
    
        
    print'done'