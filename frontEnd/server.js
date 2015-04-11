var express = require('express'),
	docs = require('./routes/docs'),/*,
	bodyParser = require('body-parser');*/
	setImmediate = global.setImmediate;

var app = express();

//root='/Users/Jon/Code/DataKind/GlobalGiving/nasaMining/frontEnd'

app.get('/', function (req, res) {
	//res.send('Hello world')
	res.sendfile('public/index.html');
});
app.get('/getDatasets', docs.getDatasets);

/*app.get('/^(.+)$/', function(req,res){
	res.sendFile(root+'/public/' + req.params[0]);
});*/

/*
var allowCrossDomain = function(req, res, next){
	res.header('Access-Control-Allow-Origin', "*");
	res.header('Access-Control-Allow-Methods', "GET,POST");
	res.header('Access-Control-Allow-Headers', "Content-Type");
}
app.use(allowCrossDomain);
app.use(bodyParser({'limit':'50mb'}));


app.get('/', function(req,res){
	res.sendfile('public/index.html');
});

app.get('/^(.+)$/', function(req,res){
	res.sendfile('public/' + req.params[0]);
});
*/
var server = app.listen(3000, '127.0.0.1', function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});