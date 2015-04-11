from __future__ import unicode_literals
import json
from gensim.models.phrases import Phrases
from textblob import TextBlob


# from gensim: threshold represents a threshold for forming the phrases (higher means fewer phrases).
# A phrase of words a and b is accepted if (cnt(a, b) - min_count) * N / (cnt(a) * cnt(b)) > threshold, where N is the total vocabulary size.
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
            dataset[doc]['gensim_bigram_kw'] = set()

        for kw in filter(lambda k: '_' in k, bigram):
            keyword = kw.replace('_', ' ').lower()

            # filter out punctuation, etc (make sure that there are two non-punc words)
            if len(TextBlob(keyword).words) != 2:
                continue

            dataset[doc]['gensim_bigram_kw'].add(kw.replace('_', ' ').lower())

    # convert set into list for json serialization
    for d in dataset:
        d['gensim_bigram_kw'] = list(d['gensim_bigram_kw'])

    # update the original data json and save
    data['dataset'] = dataset
    with open('data/nasa_bigram.json', 'w') as f:
        json.dump(data, f)