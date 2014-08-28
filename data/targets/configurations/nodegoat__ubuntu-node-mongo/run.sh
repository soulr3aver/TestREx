#!/bin/bash
mongod &
sleep 5 #change this to check if mongo is ready
mongo < nodegoat_db_reset.js
#cd /var/www | grunt run
PORT=8888 nodejs /var/www/server.js
