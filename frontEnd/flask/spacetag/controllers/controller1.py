#!./venv/bin/python

# from flask import request #, make_response
from collections import Counter

from flask import request, render_template, make_response

from time import time
import httplib
import urllib
import json
import re
import pymongo
from pymongo import MongoClient
from spacetag import app
from . import valueFromRequest


@app.route('/', defaults={'path': ''})
@app.route('/')
def index():
    ''' This shows how to render a template. '''

    templateDict = {}
    return render_template("index.html", **templateDict)


@app.route('/getCoOccuringKWsFlat', methods=['GET', 'POST'])
def getCoOccuringKWsFlat():
    query = valueFromRequest(key="q", request=request)

    if not query:
        response = make_response(json.dumps({"error": 'you must pass in a query, of form q='}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.keywords.find(
        {"source": "http://data.nasa.gov/data.json", "keyword": re.compile(r'^' + query, re.IGNORECASE)},
        {"_id": 0})

    if not results:
        response = make_response(json.dumps([]))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    keywords = Counter()
    for result in results:
        keywords.update(result['keywords_full'])

    results = sorted([{'kw': k, 'count': v} for k, v in keywords.iteritems()], key=lambda kw: kw['count'], reverse=True)

    response = make_response(json.dumps(results))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getEdges', methods=['GET', 'POST'])
def getEdges():
    keywords = json.loads(valueFromRequest(key="kws", request=request))
    threshold = float(valueFromRequest(key="threshold", default=-0.5, request=request))

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.nasa_np_strengths_b.find(
        {'keyword': {"$in": keywords}, 'count': {'$gt': 1}, 'pmi_doc': {'$gte': threshold}},
        {'_id': 0})

    if not results:
        response = make_response(json.dumps([]))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    names = []
    nameDict = dict()
    counter = 0
    edges = []

    for result in results:
        t1, t2 = result['keyword']
        if t1 not in nameDict:
            nameDict[t1] = counter
            counter += 1
            names.append({'name': t1, 'num': result['a']})

        if t2 not in nameDict:
            nameDict[t2] = counter
            counter += 1
            names.append({'name': t2, 'num': result['b']})

        edges.append({'source': nameDict[t1], 'target': nameDict[t2], 'value': result['pmi_doc'] + 1})

    response = make_response(json.dumps({'nodes': names, 'links': edges,
                                         'query': {'keyword': {"$in": keywords}, 'count': {'$gt': 1},
                                                   'pmi_doc': {'$gte': threshold}}}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getCoOccuringKWsGraph', methods=['GET', 'POST'])
def getCoOccuringKWsGraph():
    query = valueFromRequest(key="q", request=request)
    threshold = float(valueFromRequest(key="threshold", default=-0.5, request=request))

    if not query:
        response = make_response(json.dumps({"error": 'you must pass in a query, of form q='}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.keywords.find(
        {"source": "http://data.nasa.gov/data.json", "keyword": re.compile(r'^' + query, re.IGNORECASE)},
        {"_id": 0})

    if not results:
        response = make_response(json.dumps([]))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    keywords = Counter()
    for result in results:
        keywords.update(result['keywords_full'])

    min_count = keywords.most_common(1)[0][1] / 2.

    keywords = [k[0] for k in keywords.iteritems() if k[1] >= min_count]

    results = db.nasa_np_strengths_b.find(
        {'keyword': {"$in": keywords}, 'count': {'$gt': 1}, 'pmi_doc': {'$gte': threshold}},
        {'_id': 0})

    if not results:
        response = make_response(json.dumps([]))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    names = []
    nameDict = dict()
    counter = 0
    edges = []

    for result in results:
        t1, t2 = result['keyword']
        if t1 not in nameDict:
            nameDict[t1] = counter
            counter += 1
            names.append({'name': t1, 'num': result['a']})

        if t2 not in nameDict:
            nameDict[t2] = counter
            counter += 1
            names.append({'name': t2, 'num': result['b']})

        edges.append({'source': nameDict[t1], 'target': nameDict[t2], 'value': result['pmi_doc'] + 1})

    response = make_response(json.dumps({'nodes': names, 'links': edges}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getDatasets', methods=['GET', 'POST'])
def getDatasets():
    query = valueFromRequest(key="q", request=request)

    if not query:
        response = make_response(json.dumps({"error": 'you must pass in a query, of form q='}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    fields = {
        'title': 1,
        'issued': 1,
        'identifier': 1,
        'keyword': 1,
        'description_ngram_np': 1,
        'title_ngram_np': 1,
        'description': 1,
        'landingPage': 1,
        'publisher.name': 1,
        'distribution': 1,
        'source': 1
    }

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.datasets.find({"description_ngram_np": query}, fields)
    # results = []

    # try:
    #     results = db.datasets.find({"description_ngram_np": query})
    # except:
    #     results = []

    if not results:
        response = make_response(json.dumps({'query': query, 'fields': fields}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    # if not results:
    #     results = db.datasets.find({"description_ngram_np": query.upper()}, fields)

    response = make_response(json.dumps(results))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getRelatedDatasets', methods=['GET', 'POST'])
def getRelatedDatasets():
    identifier = valueFromRequest(key="identifier", request=request)

    if not identifier:
        response = make_response(json.dumps({"error": 'you must pass in an identifier'}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.related_datasets.find({'identifier': identifier}, {'_id': 0}).sort([('sim', -1)])

    response = make_response(json.dumps(results))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getDatasetsByIdentifier', methods=['GET', 'POST'])
def getDatasetsByIdentifier():
    identifiers = valueFromRequest(key="ids", list=True, request=request)

    if not identifiers:
        response = make_response(json.dumps({"error": 'you must pass in an identifier'}))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Content-Type'] = 'application/json'
        return response

    client = MongoClient('proximus.modulusmongo.net:27017')
    client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
    db = client.tepO9seb

    results = db.datasets.find({'identifier': {'$in': identifiers}}, {'_id': 0, "landingPage": 1, "title": 1})

    response = make_response(json.dumps(results))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'application/json'
    return response