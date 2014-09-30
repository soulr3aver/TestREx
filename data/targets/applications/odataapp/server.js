var express = require("express"),
	http = require("http"),
	path = require("path"),
	routes = require("./routes"),
	port = process.argv[2] || 8888;
require("jaydata");
require("q");
require("./model");
window.DOMParser = require('xmldom').DOMParser;
	
var server = express();

server.configure(function() {
	server.use(express.static(__dirname + "/public/client"));
	server.use(express.json());
	server.use(express.urlencoded());
	server.use(express.favicon());
	server.use(express.logger('dev'));
	server.use(express.methodOverride());
	server.use(server.router);
	server.use(express.query());
	server.use(express.bodyParser());
	server.use(express.cookieParser());
	server.use(express.session({ secret: 'session key' }));
	server.use("/myservice", $data.JayService.OData.Utils.simpleBodyReader());
	server.use("/myservice", $data.JayService.createAdapter(myservice.Context, function (req, res) {
    	return new myservice.Context({name: "mongoDB", databaseName:"goods", address: "localhost", port: 27017 });
	}));
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
