To run the stuff:

1. Modify "package.json" to add new dependencies of node.js (NOT necessary);
2. To install node.js dependencies type:
	-> npm install -d
3. Type "mysql -u root -ptoor" to opem MySQL console and type the following commands:
	-> CREATE DATABASE IF NOT EXISTS SQLInjection;
	-> USE SQLInjection;
	-> CREATE TABLE users(id VARCHAR(28), pword VARCHAR(28));	
5. Exit MySQL console and type:
	-> mysqlimport -u root -ptoor --local SQLInjection users.txt
4. To start the application type:
	-> node server [port]

