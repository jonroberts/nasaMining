from __future__ import unicode_literals
import json
from nltk.tokenize.treebank import TreebankWordTokenizer
from gensim.models.phrases import Phrases
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from textblob import TextBlob


if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']

    print len(dataset), 'datasets'

    # tokenize description fields
    print 'Tokenizing descriptions'
    desc = []
    for ds in dataset:
        text = TextBlob(ds['description'])
        for sentence in text.sentences:
            desc.append(sentence.tokens)

    print 'Constructing bigrams'
    desc_bigrams = Phrases(desc)
    bigrams = desc_bigrams[desc]

    # tokenizer = TreebankWordTokenizer()
    # desc = [tokenizer.tokenize(d['description']) for d in dataset]
    #
    # # collocations
    # desc_bigrams = Phrases(desc)
    # desc_trigrams = Phrases(desc_bigrams[desc])
    #
    # bigrams = desc_bigrams[desc]
    # trigrams = desc_trigrams[bigrams]
    #
    # # textrank
    # stemmer = Stemmer('english')
    # summarizer = Summarizer(stemmer)
    # summarizer.stop_words = get_stop_words('english')
    # tokenizer2 = Tokenizer('english')
    #
    # parser = PlaintextParser(dataset[0]['description'], tokenizer2)