from __future__ import unicode_literals
import requests
import json


states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
    'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming'
]


if __name__ == '__main__':
    for state in states:
        s = state.lower().replace(' ', '')
        url = 'http://data.%s.gov/data.json' % s
        print url

        try:
            res = requests.get(url)

            if res.status_code == 200:
                data = res.json()

                with open('data/%s.json' % s, 'w') as f:
                    json.dump(data, f)
        except:
            print '\tError'

            if ' ' in state:
                s = ''.join([s_[0] for s_ in state.split()]).lower()
                url = 'http://data.%s.gov/data.json' % s
                print '\tTrying %s' % url

                try:
                    res = requests.get(url)

                    if res.status_code == 200:
                        data = res.json()

                        with open('data/%s.json' % s, 'w') as f:
                            json.dump(data, f)
                except:
                    print '\tError'
                    pass