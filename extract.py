from __future__ import unicode_literals
import json
from gensim.models.phrases import Phrases
from textblob import TextBlob
import cPickle as pickle


def parse_input(input_json, input_source=None):
    print input_json, ': Tokenizing descriptions'

    desc = []
    doc_id = []
    dataset = json.load(open(input_json))['dataset']

    for i, ds in enumerate(dataset):
        if input_source:
            ds['source'] = input_source

        text = TextBlob(ds['description'])
        for sentence in text.sentences:
            desc.append(sentence.tokens)
            doc_id.append(i)

    return dataset, desc, doc_id


def construct_ngrams(desc, desc_seed=None, phrase_passes=5, phrase_threshold=10, model_output=None):
    models = []
    desc_seed = desc_seed or []

    print 'Constructing ngrams'
    for i in range(phrase_passes):
        print '\t', i
        model = Phrases(desc + desc_seed if i == 0 else desc, threshold=phrase_threshold)
        desc = model[desc]
        models.append(model)

    if model_output:
        with open(model_output, 'wb+') as f:
            pickle.dump(models, f)

    return desc


def extract(ngrams, dataset, doc_id):
    # extract keywords
    print 'Extracting keywords'
    for i, ngram in enumerate(ngrams):
        doc = doc_id[i]

        if field not in dataset[doc]:
            dataset[doc][field] = set()

            if doc > 0 and doc % 1000 == 0:
                print '\t', doc

        for kw in filter(lambda k: '_' in k, ngram):
            keyword = kw.replace('_', ' ')

            kw_tb = TextBlob(keyword)

            # filter out punctuation, etc (make sure that there are two non-punc words)
            if len(kw_tb.words) < 2:
                continue

            # add keywords which are all proper nouns
            distinct_tags = set(t[1] for t in kw_tb.tags)
            if distinct_tags - {'NNP', 'NNPS'} == {}:
                dataset[doc][field].add(kw_tb.lower())
                continue

            # add noun phrases
            for np in kw_tb.lower().noun_phrases:
                dataset[doc][field].add(np)

    return kw_set_to_list(dataset)


def kw_set_to_list(dataset):
    # convert set into list for json serialization
    for d in dataset:
        d[field] = list(d[field])

        # fix 's
        for i, np in enumerate(d[field]):
            if np.endswith(" 's"):
                np = np[:-3]

            if np.startswith("'s "):
                np = np.replace("'s ", "", 1)

            np = np.replace(" 's", "'s")

            d[field][i] = np
        d[field] = list(set(d[field]))

    return dataset


if __name__ == '__main__':
    input_json = 'data/defense.json'
    input_source = 'defense.gov/data.json'
    seed_json = 'data/nasa.json'
    output_file = 'data/defense_ngram_np2.json'
    model_output = 'models.pkl'
    field = 'description_ngram_np'
    phrase_passes = 5
    phrase_threshold = 10

    # parse input data
    dataset, desc, doc_id = parse_input(input_json, input_source)

    # parse secondary seed data
    desc_seed = []
    if seed_json:
        _, desc_seed, _ = parse_input(seed_json)

    ngrams = construct_ngrams(desc, desc_seed, phrase_passes, phrase_threshold, model_output)

    dataset = extract(ngrams, dataset, doc_id)

    with open(output_file, 'w') as f:
        json.dump(dataset, f)