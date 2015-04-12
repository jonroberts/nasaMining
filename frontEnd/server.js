var express = require('express'),
	docs = require('./routes/docs'),/*,
	bodyParser = require('body-parser');*/
	setImmediate = global.setImmediate;

var app = express();
app.get('/', function (req, res) {
	//res.send('Hello world')
	res.sendfile('public/index.html');
});
app.get('/getDatasets', docs.getDatasets);
app.get('/getCoOccuringKWs', docs.getCoOccuringKWs);
app.get('/getCoOccuringKWsMulti', docs.getCoOccuringKWsMulti);
app.get('/getEdges', docs.getEdges);
app.get(/^(.+)$/, function(req,res){
	res.sendfile('public/' + req.params[0]);
});

var server = app.listen(3000, '127.0.0.1', function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});