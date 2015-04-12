var mongojs = require("mongojs")({});
var db = require("mongojs")
    .connect('mongodb://nasahack:hacking4nasa@proximus.modulusmongo.net:27017/tepO9seb',
    ['datasets', 'kw_pair_freq','nasa_np_strengths_b']);


exports.getDatasets = function (req,res){
	var query=req.query.q;
	var using=req.query.field;
	var field=(using==undefined)?'keyword':using;
	console.log(field);
	var theQuery={};
	theQuery[field]=query;
	console.log(theQuery);
	var theFields={'title':1,'issued':1,'identifier':1,'keyword':1,'description_ngram_np':1,'title_ngram_np':1,'description':1,'landingPage':1,'publisher.name':1,'distribution':1};
	if (query==undefined) res.send({'error':'you must pass in a query, of form q='})
	else{
		db.datasets.find(theQuery,theFields,function(err,docs){
			if(docs.length==0){
				theQuery[field]=query.toUpperCase();
				db.datasets.find(theQuery,theFields,function(err,docs){
					res.send(docs);
				})
			}
			else{
				res.send(docs);
			}
		})
	}
}

exports.getEdges = function(req,res){
	var keywords=JSON.parse(req.query.kws);
	var threshold=(req.query.threshold==undefined)?-0.5:req.query.threshold;
	var using=req.query.field;
	var field=(using==undefined)?'keyword':using;

	console.log(keywords);
	if(field=='keyword'){
		db.kw_pair_freq.find({'keyword':{"$in":keywords},'count':{'$gt':1}},{'_id':0},function(err,docs){
			var names=[];
			var nameDict={};
			var counter=0;
			var edges=[];
			for(var dx in docs){
				var d=docs[dx];
				if(d['pmi_doc']<threshold) continue;
	
				var t1=d['keyword'][0];
				var t2=d['keyword'][1];
				if(nameDict[t1]==undefined){
					nameDict[t1]=counter;
					counter+=1;
					names.push({'name':t1,'num':d['a']});
				}
				if(nameDict[t2]==undefined){
					nameDict[t2]=counter;
					counter+=1;
					names.push({'name':t2,'num':d['b']});
				}
				edges.push({'source':nameDict[t1],'target':nameDict[t2],'value':d['pmi_doc']+1});
			}
			res.send({'nodes':names,'links':edges});
		})
	}
	else{
		db.nasa_np_strengths_b.find({'keyword':{"$in":keywords},'count':{'$gt':1}},{'_id':0},function(err,docs){
			var names=[];
			var nameDict={};
			var counter=0;
			var edges=[];
			for(var dx in docs){
				var d=docs[dx];
				if(d['pmi_doc']<threshold) continue;
	
				var t1=d['keyword'][0];
				var t2=d['keyword'][1];
				if(nameDict[t1]==undefined){
					nameDict[t1]=counter;
					counter+=1;
					names.push({'name':t1,'num':d['a']});
				}
				if(nameDict[t2]==undefined){
					nameDict[t2]=counter;
					counter+=1;
					names.push({'name':t2,'num':d['b']});
				}
				edges.push({'source':nameDict[t1],'target':nameDict[t2],'value':d['pmi_doc']+1});
			}
			res.send({'nodes':names,'links':edges});
		})
	}

}

exports.getCoOccuringKWs = function(req,res){
	var query=req.query.q;
	console.log(query);
	var using=req.query.field;
	var field=(using==undefined)?'keyword':using;
	var searches={'keyword':function(curr,result){
				  		  		for(var kx in curr['keyword']){
				  		  			var kw=curr['keyword'][kx];
				  		  			if(result[kw]==undefined){
				  		  				result[kw]=1;
				  		  			}
				  		  			else{
				  		  				result[kw]+=1;
				  		  			}
				  		  		}
				  		  	},
				  	'description_textrank_kw':function(curr,result){
				  		  		for(var kx in curr['description_textrank_kw']){
				  		  			var kw=curr['description_textrank_kw'][kx];
				  		  			if(result[kw]==undefined){
				  		  				result[kw]=1;
				  		  			}
				  		  			else{
				  		  				result[kw]+=1;
				  		  			}
				  		  		}
				  		  	},
				  	'description_bigram_kw':function(curr,result){
				  		  		for(var kx in curr['description_bigram_kw']){
				  		  			var kw=curr['description_bigram_kw'][kx];
				  		  			if(result[kw]==undefined){
				  		  				result[kw]=1;
				  		  			}
				  		  			else{
				  		  				result[kw]+=1;
				  		  			}
				  		  		}
				  		  	},
				  	'description_ngram_np':function(curr,result){
				  		  		for(var kx in curr['description_ngram_np']){
				  		  			var kw=curr['description_ngram_np'][kx];
				  		  			if(result[kw]==undefined){
				  		  				result[kw]=1;
				  		  			}
				  		  			else{
				  		  				result[kw]+=1;
				  		  			}
				  		  		}
				  		  	}				  		  	
				  	}
				  	
	var theQuery={'key':{},
			      'cond': {"source": "http://data.nasa.gov/data.json"},
				  'reduce':searches[field],
				  'initial':{}
				 };
	theQuery['cond'][field]={"$regex":new RegExp('^'+query, 'i')};

	if (query==undefined) res.send({'error':'you must pass in a query, of form q='})
	else{
		db.datasets.group(theQuery,function(err,docs){
			if(err|!docs) res.send({'error':'no documents found'});
			else{
				var values=docs[0];
				var results=[];
				for(var k in values) {results.push({'kw':k,'count':values[k]});}
				results.sort(function(a,b){return +b.count-a.count;});
	
				res.send(results);
			}
		})
	}
	
}

exports.getCoOccuringKWsMulti = function (req, res) {
    var keywords = JSON.parse(req.query.kws);
    var using = req.query.field;
    var field = (using == undefined) ? 'keyword' : using;
    var searches = {
        'keyword': function (curr, result) {
            for (var kx in curr['keyword']) {
                var kw = curr['keyword'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_textrank_kw': function (curr, result) {
            for (var kx in curr['description_textrank_kw']) {
                var kw = curr['description_textrank_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_bigram_kw': function (curr, result) {
            for (var kx in curr['description_bigram_kw']) {
                var kw = curr['description_bigram_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
	  	'description_ngram_np':function(curr,result){
	  		for(var kx in curr['description_ngram_np']){
	  			var kw=curr['description_ngram_np'][kx];
	  			if(result[kw]==undefined){
	  				result[kw]=1;
	  			}
	  			else{
	  				result[kw]+=1;
	  			}
	  		}
	  	}				  		  	
    };

    var theQuery = {
        'key': {},
        'cond': {"source": "http://data.nasa.gov/data.json"},
        'reduce': searches[field],
        'initial': {}
    };
    theQuery['cond'][field] = {"$in": keywords};

    if (keywords == undefined) res.send({'error': 'you must pass in a query, of form q='});
    else {
        db.datasets.group(theQuery, function (err, docs) {
            var values = docs[0];
            var results = [];
            for (var k in values) {
                results.push({'kw': k, 'count': values[k]});
            }
            results.sort(function (a, b) {
                return +b.count - a.count;
            });

            res.send(results);
        })
    }

};