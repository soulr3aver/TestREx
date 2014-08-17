var mysql = require("mysql");


var mysqlProvider = function(hostName, dbName, userName, pword) {
	this.connection = mysql.createConnection({host : hostName, database: dbName, user : userName, password : pword});
	this.connection.connect();
	this.connection.on("error", function(error) {
		this.connection.destroy();
		console.log("DB ERROR: " + error);
	});
}
    
mysqlProvider.prototype.sendQuery = function(queryStr, param, callback) {
	
	this.connection.query(queryStr, param, function(error, results) {
		if (error) {
			console.log("ERROR: " + error);
			callback(error);
		}
		callback(null, results);
	});
}

exports.mysqlProvider = mysqlProvider;
