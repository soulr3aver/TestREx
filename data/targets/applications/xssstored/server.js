var express = require("express"),
	http = require("http"),
	path = require("path"),
	routes = require("./routes"),
	comments = require("./routes/comments"),
	mongoProvider = require("./dbproviders/mongoProvider").mongoProvider;
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
	//server.set("views", __dirname + "/views");
	//server.engine("html", require("ejs").renderFile);
});

server.configure('development', function(){
  server.use(express.errorHandler());
});

// Init db provider --------------------------------
var dbprovider = new mongoProvider("blogpost","localhost", 27017);
// Assign routes -----------------------------------
server.get("/", routes.index);
server.post("/comments.html", comments.addComment)
//--------------------------------------------------

// Start the server --------------------------------
http.createServer(server).listen(port, function() {	
	console.log("Server started on port: " + port);
});

exports.dbprovider = dbprovider;
