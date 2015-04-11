from __future__ import unicode_literals
import json
from gensim.models.phrases import Phrases
from textblob import TextBlob


bigram_thresh = 10

if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']

    print len(dataset), 'datasets'

    # tokenize description fields
    print 'Tokenizing descriptions'
    desc = []
    doc_id = []
    for i, ds in enumerate(dataset):
        text = TextBlob(ds['description'])
        for sentence in text.sentences:
            desc.append(sentence.tokens)
            doc_id.append(i)

    print 'Constructing bigrams'
    desc_bigrams = Phrases(desc, threshold=bigram_thresh)
    bigrams = desc_bigrams[desc]

    # pull out bigram keywords
    for i, bigram in enumerate(bigrams):
        doc = doc_id[i]

        if 'gensim_bigram_kw' not in dataset[doc]:
            dataset[doc]['gensim_bigram_kw'] = list()

        for kw in filter(lambda k: '_' in k, bigram):
            dataset[doc]['gensim_bigram_kw'].append(kw.split('_'))

    # update the original data json and save
    data['dataset'] = dataset
    with open('data/nasa_bigram.json', 'w') as f:
        json.dump(data, f)