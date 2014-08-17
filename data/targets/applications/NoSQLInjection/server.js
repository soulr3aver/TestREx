var express = require("express"),
	http = require("http"),
	path = require("path"),
	routes = require("./routes"),
	restricted = require("./routes/restricted"),
	port = process.argv[2] || 8888,
	mongoProvider = require("./dbproviders/mongoProvider").mongoProvider;
	
var server = express();

server.configure(function() {
	server.use(express.static(__dirname + "/public/client"));
	server.use(express.json());
	server.use(express.urlencoded());
	server.use(express.favicon());
	server.use(express.logger('dev'));
	server.use(express.methodOverride());
	server.use(server.router);
	//server.use(require('stylus').middleware(path.join(__dirname, 'public')));
});

server.configure('development', function(){
  server.use(express.errorHandler());
});

// Init db provider --------------------------------
var dbName = "nosqlInj";
var dbprovider = new mongoProvider(dbName,"localhost", 27017);

// Assign routes -----------------------------------
server.get("/", routes.index);
server.post("/secure", restricted.secure);
server.post("/insecure", restricted.insecure);

//--------------------------------------------------

// Start the server --------------------------------
http.createServer(server).listen(port, function() {	
	console.log("Server started on port: " + port);
});

exports.dbprovider = dbprovider;
