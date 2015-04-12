from __future__ import unicode_literals
import json, operator
from itertools import combinations
from math import log

# generate a list of frequency counts for keyword pairs, sorted in reverse order by total
if __name__ == '__main__':
    infile = 'data/states_ngram_np.json'
    outfile = 'data/states_np_strengths.json'
    data = json.load(open(infile))
#     kw_field = 'keyword'
#     kw_field = 'description_textrank_kw'
#     kw_field = 'description_bigram_kw'
    kw_field = 'gensim_ngram_np'
    dataset = data['dataset']
    keyholder = {}
    outdata = []

    pairs = {}
    single_words = {}
    for i, ds in enumerate(dataset):
        for pair in combinations(ds[kw_field], 2):
            sl_pair = sorted([x.lower() for x in pair], key=unicode.lower)
            
            if sl_pair[0] != sl_pair[1]: # there are projects with duplicate keywords in the metadata
                
                key = str(sl_pair)
                keyholder[key] = sl_pair
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 1;
                    
                # left word
                if sl_pair[0] in single_words:
                    single_words[sl_pair[0]] += 1
                else:
                    single_words[sl_pair[0]] = 1
    
                # right word, probly a better way to do this
                if sl_pair[1] in single_words:
                    single_words[sl_pair[1]] += 1
                else:
                    single_words[sl_pair[1]] = 1
    
    for pair, count in sorted(pairs.items(), key=operator.itemgetter(1), reverse=True):
        cA = single_words[keyholder[pair][0]] # total count of the first word
        cB = single_words[keyholder[pair][1]] # total count of the second word
        cAB = float(count)
        
        # if A and B only occur together once (this happens), then avoid a ZeroDivisionError.
        #    if A and B individually each appear only 1 time, then this is significant (set to 1), otherwise it 
        #    is probably not significant at all (set to 0)

        if cAB == 1:
            if cA == 1 and cB == 1:
                dpmi = 1
                kpmi = 1
            else:
                dpmi = 0
                kpmi = 0
        else:
            dpmi = log((cAB * len(dataset)) / (cA * cB), 10) / -1 * log(cAB / len(dataset), 10)
            kpmi = log((cAB * len(single_words)) / (cA * cB), 10) / -1 * log(cAB / len(single_words), 10)
        outdata.append({'keyword': keyholder[pair], 'count': cAB, 'a': cA, 'b': cB, 'pmi_doc': dpmi, 'pmi_kw': kpmi})
        
    with open(outfile, 'w') as f:
        json.dump(outdata, f)
        
    print 'done'