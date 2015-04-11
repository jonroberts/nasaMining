from __future__ import unicode_literals
import json
from nltk.tokenize.treebank import TreebankWordTokenizer
from gensim.models.phrases import Phrases
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words



if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']

    print len(dataset)

    tokenizer = TreebankWordTokenizer()
    desc = [tokenizer.tokenize(d['description']) for d in dataset]

    # collocations
    desc_bigrams = Phrases(desc)
    desc_trigrams = Phrases(desc_bigrams[desc])

    bigrams = desc_bigrams[desc]
    trigrams = desc_trigrams[bigrams]

    # textrank
    stemmer = Stemmer('english')
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')
    tokenizer2 = Tokenizer('english')

    parser = PlaintextParser(dataset[0]['description'], tokenizer2)