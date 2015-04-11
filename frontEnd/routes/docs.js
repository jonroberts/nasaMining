var mongojs = require("mongojs")({});
var db = require("mongojs")
		.connect('mongodb://nasahack:hacking4nasa@proximus.modulusmongo.net:27017/tepO9seb',
		['datasets']);

exports.getDatasets = function (req,res){
	var query=req.query.q;
	var using=req.query.field;
	var field=(using==undefined)?'keyword':using;
	console.log(field);
	var theQuery={};
	theQuery[field]=query;

	if (query==undefined) res.send({'error':'you must pass in a query, of form q='})
	else{
		db.datasets.find(theQuery,{'title':1},function(err,docs){
			res.send(docs);
		})
	}
}

exports.getCoOccuringKWs = function(req,res){
	var query=req.query.q;
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
				  		  	}
				  	}
				  	
	var theQuery={'key':{},
				  'cond':{},
				  'reduce':searches[field],
				  'initial':{}
				 };
	theQuery['cond'][field]={"$regex":new RegExp('^'+query, 'i')};

	if (query==undefined) res.send({'error':'you must pass in a query, of form q='})
	else{
		db.datasets.group(theQuery,function(err,docs){
			var values=docs[0];
			var results=[];
			for(var k in values) {results.push({'kw':k,'count':values[k]});}
			results.sort(function(a,b){return +b.count-a.count;});

			res.send(results);
		})
	}
	
}
