from __future__ import unicode_literals
import json, operator
from itertools import combinations
from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora

if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']
    descs = []

    # create a list o descriptions
    for i, ds in enumerate(dataset):
        descs.append(ds['description'])

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in desc.lower().split() if word not in stoplist] for desc in descs]
        
    # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.save('/dicts/nasa.dict')
    print dictionary
    
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/dicts/nasa.mm', corpus)

#     dictionary = corpora.Dictionary(descs)
#     raw_corpus = [dictionary.doc2bow(t) for t in descs]
    
#     tfidf = TfidfModel(descs)
#     print(tfidf['atmosphere'])
#     
        
    print'done'