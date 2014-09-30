var db = require("mongodb").Db,
	connection = require("mongodb").Connection,
	mongoServer = require("mongodb").Server,
	bson = require("mongodb").BSON,
	objectId = require("mongodb").ObjectID;


var mongoProvider = function(dbname, host, port) {
	this.db = new db(dbname, new mongoServer(host, port, {safe: false}, {auto_reconnect: true}, {}));
	this.db.open(function(){});
}

mongoProvider.prototype.getCollection = function(collection, callback) {
	this.db.collection(collection, function(error, usersColl) {
		if (error) {
			callback(error);
		}
		else {
			callback(null, usersColl);
		}
	});
}

mongoProvider.prototype.findOne = function(collection, criteria, callback) { 
	this.getCollection(collection, function(error, collection) {
		if (error) {
			callback(error);
		}
		else {
			collection.findOne(criteria, function(erorr, item) {
				if (error) {
					callback(error);
				}
				else {
					callback(null, item);
				}
			});
		}
	});	
}


mongoProvider.prototype.findAll = function(collection, callback) {
	this.getCollection(collection, function(error, collection) {
		if (error) {
			callback(error);
		}
		else {
			collection.find().toArray(function(error, results) {
				if (error) {
					callback(error);
				}
				else {
					callback(null, results);
				}
			});
		}
	});
}
exports.mongoProvider = mongoProvider;