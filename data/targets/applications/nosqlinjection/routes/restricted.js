var server = require("../server");

/*
* POST restricted resource - secure implementation
*  db.users :
*  { _id : "userid", pword : "password"}
*/
exports.secure = function(request, response) {
	var loginRegex = new RegExp("^[a-zA-Z0-9]+$");
	var login = request.body.userid;
	var password = request.body.passwd;
	
	server.dbprovider.findOne("users", {_id : login}, function(error, item) {
		if (error != null) {
			response.send("MongoDB ERROR: " + error);			
			return;
		}			
		if (!login.match(loginRegex) || item == null || item.pword != password) {
			response.send("Access denied!");
		}
		else {
			response.send("Hello, " + item._id + "!");
		}
	});
}

/*
* POST restricted resource - insecure implementation
*  db.users :
*  { _id : "userid", pword : "password"}
*
*  Possible injections:
*  --> Batman'})//	<--
*  --> ' + response.send("Your website sucks!") + '})// <--
*  --> ' + server.dbprovider.findAll("users", function(error, results) {response.send(results)}) + '})// <--
*/
exports.insecure = function(request, response) {
	var login = request.body.userid;
	var password = request.body.passwd;
	var loginParam = eval("({ _id: '" + login + "', pword : '" + password + "'})");
	
	server.dbprovider.findOne("users", loginParam, function(error, item) {	
		if (error != null) {
			response.send("MongoDB ERROR: " + error);			
			return;
		}
		if (item != null) {
			response.send("Hello, " + item._id + "!");
		}
		else {
			response.send("Access denied!");
		}
	});
}
