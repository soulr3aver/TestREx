#!/bin/bash
mongod & 
sleep 5 #change this to check if mongo is ready 
mongoimport --db nosqlInj --collection users --jsonArray mongoData.json 
nodejs /var/www/server.js
