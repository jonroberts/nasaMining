import json
from nltk.corpus import wordnet as wn
from itertools import combinations

if __name__ == '__main__':
    data = json.load(open('data/nasa_kw.json'))
    outfile = 'data/keyword_synset_scores.json'
    kw_field = 'keyword'
    max_items = 700000 # limit keyword pairs to analyse. there are ~1100 projects, that's ~640000 pairs!
    dataset = data['dataset']
    similarity = []
    single_words = []

    # create a list of all single words among keywords
    for i, ds in enumerate(dataset):
        for keyword in ds[kw_field]:
            for one_word in keyword.lower().split():
                if one_word not in single_words:
                    single_words.append(one_word)

    # create a matrix of all similarity scores
    #
    # for all unique pairs of keyword words:
    #    compare each word in the synset of the first with that of the second
    #    keep the highest similarity score, let that be the score for those two words
    #
    #    0 if at least one of the words is not in WordNet
    #
    # 1134 words have 642411 unique pairs
#     count = 0
    for pair in list(combinations(single_words, 2))[:max_items]:
        key = str(sorted(pair, key=unicode.lower))
        if key not in similarity:
            score = 0.0
            if pair[0] == pair[1]:
                score = 1.0
            else:
                for word1 in wn.synsets(pair[0]):
                    for word2 in wn.synsets(pair[1]):
                        score = max([score, word1.path_similarity(word2)])
            similarity.append({'keyword': pair, 'score': score})
    #             print count # sanity check for long runs
    #             count += 1
    
    with open(outfile, 'w') as f:
        json.dump(similarity, f)
        
    print 'done'
    # calculate a score for each pair of projects in the dataset
    #
    # score = sum of keyword similarities for all pairs of keywords 
#     print len(dataset)
#     print len(single_words)
#     print similarity

#    [i for i,x in enumerate(testlist) if x == 1]

 
#     print score