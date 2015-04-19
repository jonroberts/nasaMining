from __future__ import unicode_literals
import json
import string
from gensim.models.phrases import Phrases
from textblob import TextBlob
from textrank import extractKeyphrases
from joblib import Parallel, delayed


def bigram_kw(data, field='description', threshold=10):
    # tokenize description fields
    print 'Tokenizing'
    desc = []
    doc_id = []
    for i, ds in enumerate(data):
        text = TextBlob(ds[field])
        for sentence in text.sentences:
            desc.append(sentence.tokens)
            doc_id.append(i)

    print 'Constructing bigrams'
    desc_bigrams = Phrases(desc, threshold=threshold)
    bigrams = desc_bigrams[desc]

    # pull out bigram keywords
    print 'Extracting keywords'

    kw_field = '%s_bigram_kw' % field
    for i, bigram in enumerate(bigrams):
        doc = doc_id[i]

        if kw_field not in data[doc]:
            data[doc][kw_field] = set()

        for kw in filter(lambda k: '_' in k, bigram):
            keyword = kw.replace('_', ' ').upper()

            # filter out punctuation, etc (make sure that there are two non-punc words)
            if len(TextBlob(keyword).words) != 2:
                continue

            data[doc][kw_field].add(keyword)

    # convert set into list for json serialization
    for d in data:
        d[kw_field] = list(d[kw_field])

    return data


def textrank_kw(data, field='description'):
    print 'Extracting textrank keywords'

    kw_field = '%s_textrank_kw' % field

    for i, d in enumerate(data):
        if i and i % 1000 == 0:
            print '\t', i

        keywords = extractKeyphrases(d[field])
        keywords = map(string.upper, keywords)
        d[kw_field] = list(set(keywords))

    return data


def textrank_parallel(text):
    keywords = extractKeyphrases(text)
    keywords = map(string.upper, keywords)
    return list(set(keywords))


if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']

    # get bigrams
    dataset = bigram_kw(dataset)

    # get textrank keywords
    # dataset = textrank_kw(dataset)

    print 'Extracting textrank keywords'
    desc = [d['description'] for d in dataset]

    textrank_kw = Parallel(n_jobs=-1, verbose=10)(delayed(textrank_parallel)(d) for d in desc)

    for d, tr in zip(dataset, textrank_kw):
        d['description_textrank_kw'] = tr

    data['dataset'] = dataset

    with open('data/nasa_kw.json', 'w') as f:
        json.dump(data, f)