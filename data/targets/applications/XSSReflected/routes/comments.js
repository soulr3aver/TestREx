var readFile = require("../helpers/fileHelper").readFile;
/*
*	POST comments
*/

exports.addComment = function(request, response) {
	readFile(request, function(contents){
		var headers = {};		
		response.writeHead(200, headers);
		response.write(contents);
		response.end();
	});	
}


