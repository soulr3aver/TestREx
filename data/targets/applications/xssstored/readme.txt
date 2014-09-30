To run the stuff:
1. Modify "package.json" to add new dependencies of node.js (NOT necessary);
2. Type "npm install -d".
3. Type "mongoimport --drop --db blogpost --collection comments --jsonArray mongoData.json" to create a corresponding data in MongoDB.
4. Start the mongoDb instance (type "mongod").
5. Type "node server [port]" to start the application.
