#!/bin/bash
mongod & 
sleep 5 #change this to check if mongo is ready 
mongoimport --drop --db blogpost --collection comments --jsonArray mongoData.json
nodejs /var/www/server.js
