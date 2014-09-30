var readFile = require("../helpers/fileHelper").readFile;
var server = require("../server");


/*
*	POST comments
* 	Possible payloads:
*   --> <script>alert("XSS")</script> <--
*   --> ' + response.send("Your website sucks") + '})// <--
*/

exports.addComment = function(request, response) {
	var newComment = request.body.newComment;
	var commentParam = eval("({ comment : '" + newComment + "'})");		// JSON injection

	server.dbprovider.save("comments", commentParam, function(error, collection, items){
		if (error != null) {
			throw error;
		}
	});

	server.dbprovider.findAll("comments", function(error, results) {
		var comments = "";

		for (i in results) {
			comments += results[i].comment + "<br/>";
		}	
		response.send(comments);										//JavaScript injection
	});		
}


