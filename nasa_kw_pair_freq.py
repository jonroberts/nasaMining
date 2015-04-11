from __future__ import unicode_literals
import json, operator
from itertools import combinations

# generate a list of frequency counts for keyword pairs, sorted in reverse order by total
if __name__ == '__main__':
    data = json.load(open('data/nasa_kw.json'))
#     kw_field = 'keyword'
#     kw_field = 'description_textrank_kw'
    kw_field = 'description_bigram_kw'
    dataset = data['dataset']
    keyholder = {}
    outdata = []

    pairs = {}
    for i, ds in enumerate(dataset):
        for pair in combinations(ds[kw_field], 2):
            sl_pair = sorted([x.lower() for x in pair], key=unicode.lower)
            key = str(sl_pair)
            keyholder[key] = sl_pair
            if key in pairs:
                pairs[key] += 1
            else:
                pairs[key] = 1;
    
    for pair, count in sorted(pairs.items(), key=operator.itemgetter(1), reverse=True):
        outdata.append({'keyword': keyholder[pair], 'count': count})
        
    with open('data/keyword_bigram_freq.json', 'w') as f:
        json.dump(outdata, f)
        
    print'done'