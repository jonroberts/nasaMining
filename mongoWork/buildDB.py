from pymongo import MongoClient
import json

data=json.load(open("/Users/Jon/Code/DataKind/GlobalGiving/nasaMining/data/nasa.json"))

client=MongoClient('proximus.modulusmongo.net:27017')
client.tepO9seb.authenticate('nasahack', 'hacking4nasa')

db=client.tepO9seb

for d in data['dataset']:
	db.datasets.insert(d)