var express = require("express"),
	http = require("http"),
	path = require("path"),
	routes = require("./routes"),
	port = process.argv[2] || 8888;
	
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

// Assign routes -----------------------------------
server.get("/", routes.index);
//--------------------------------------------------

// Start the server --------------------------------
http.createServer(server).listen(port, function() {	
	console.log("Server started on port: " + port);
});
