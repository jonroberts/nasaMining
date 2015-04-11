from __future__ import unicode_literals
import json, operator
from itertools import combinations

# generate a list of frequency counts for keyword pairs, sorted in reverse order by total
if __name__ == '__main__':
    data = json.load(open('data/nasa.json'))
    dataset = data['dataset']
    keyholder = {}
    outdata = []

    print len(dataset), 'datasets'

    # tokenize description fields
    print 'Tokenizing descriptions'
    pairs = {}
    for i, ds in enumerate(dataset):
        for pair in combinations(ds['keyword'], 2):
            sl_pair = sorted([x.lower() for x in pair], key=unicode.lower)
            key = str(sl_pair)
            keyholder[key] = sl_pair
            if key in pairs:
                pairs[key] += 1
            else:
                pairs[key] = 1;
    
    for pair, count in sorted(pairs.items(), key=operator.itemgetter(1), reverse=True):
        outdata.append({'keyword': keyholder[pair], 'count': count})
        
    with open('data/keyword_pair_freq.json', 'w') as f:
        json.dump(outdata, f)
        
    print'done'