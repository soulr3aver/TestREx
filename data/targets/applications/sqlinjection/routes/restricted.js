var server = require("../server");

/*
* POST restricted resource - secure implementation
*/
exports.secure = function(request, response) {
	var loginRegex = new RegExp("^[a-zA-Z0-9]+$");
	var login = request.body.userid;
	var password = request.body.passwd;
	
	server.dbprovider.sendQuery("SELECT pword FROM users WHERE id=?", [login], function(error, results) {
		if (error != null) {
			console.log("MySQL ERROR: " + error);
			return;
		}	
		if (!login.match(loginRegex) || results[0] == undefined || results[0].pword != password) {
			response.send("Access denied!");
		}
		else {
			response.send("Hello, " + login + "!");
		}
	});
}

/*
* POST restricted resource - insecure implementation
* Possible payloads:
* 	login --> dummy <--
* 	password --> pwned' OR 'a'='a <--
*/
exports.insecure = function(request, response) {
	var login = request.body.userid;
	var password = request.body.passwd;

	var query = "SELECT * FROM users WHERE id='" + login + "' AND pword='" + password + "'";

	server.dbprovider.sendQuery(query, null, function(error, results){
		try {
			if (error != null) {
				console.log("MySQL ERROR: " + error);
				return;
			}	
			if (results[0] == undefined) {
				response.send("Access denied!");
			}
			else {
				response.send("Hello, " + results[0].id + "!");
			}
		}
		catch (e) {
			response.send("Access denied!");
		}
	});		
}

