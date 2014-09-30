var fs = require("fs");
var server = require("../server").server;
var path = require("path");

exports.readFile = function(request, callback) {
	var filename = __dirname.replace("/helpers","") + "/public/client" + request.path;
	fs.readFile(filename, "utf8", function(error, text) {
		if (error) {
			throw error;
		}	
		callback(text);		
	});
}
