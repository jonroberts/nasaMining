var mongojs = require("mongojs")({});
var db = require("mongojs")
		.connect('mongodb://nasahack:hacking4nasa@proximus.modulusmongo.net:27017/tepO9seb',
		['datasets']);

exports.getDatasets = function (req,res){
	var query=req.query.q;
	if (query==undefined) res.send({'error':'you must pass in a query, of form q='})
	else{
		db.datasets.find({'keyword':query},{'title':1},function(err,docs){
			res.send(docs);
		})
	}
}