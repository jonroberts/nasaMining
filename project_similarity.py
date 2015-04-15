import json, operator
from numpy import column_stack
from itertools import combinations, product

if __name__ == '__main__':
    sim_data = json.load(open('data/keyword_synset_scores.json'))
    data = json.load(open('data/nasa_kw.json'))
    outfile = 'data/project_similarity_scores.json'
    dataset = data['dataset']
    kw_field = 'keyword'
    max_items = 100000 # limit project pairs to analyse. there are ~16k projects, that's ~73 million pairs!
    sim_scores = {}
    proj_sims = []

    # setup sim score hash
    for i, ds in enumerate(sim_data):
        pair = ds['keyword']
        sl_pair = str(sorted([x.lower() for x in pair], key=unicode.lower))
        sim_scores[sl_pair] = ds['score']
        
    # calculate similarity between projects
    # score = the sum of all similarity scores for each pair of keyword words 
    for proj_pair in list(combinations(dataset, 2))[:max_items]:
        
        # a fancy way to get the individual words from all the keywords in a list
        kw1 = [item for sublist in [x.lower().split() for x in proj_pair[0][kw_field]] for item in sublist]
        kw2 = [item for sublist in [x.lower().split() for x in proj_pair[1][kw_field]] for item in sublist]

        score = 0.0
        for word1 in kw1:
            for word2 in kw2:
                if word1 == word2:
                    score += 1.0
                else:
                    key = str([word1, word2])
                    if key in sim_scores:
                        score += sim_scores[key]
        
#         print '%s <=> %s: %d' % (proj_pair[0]['identifier'], proj_pair[1]['identifier'], score)
        proj_sims.append({'p1': proj_pair[0]['identifier'], 'p2': proj_pair[1]['identifier'], 'score': score})
        
        
        with open(outfile, 'w') as f:
            json.dump(sorted(proj_sims, key=operator.itemgetter('score'), reverse=True), f)

    print 'done'
    