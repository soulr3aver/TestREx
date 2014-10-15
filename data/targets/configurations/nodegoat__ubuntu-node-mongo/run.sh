#!/bin/bash
export logpath=/var/log/mongodb
export logfile=$logpath/mongodb.log
touch $logfile
mongod --quiet --logpath $logfile --logappend &

#waits until mongodb is initialized (taken from http://stackoverflow.com)
COUNTER=0
grep -q 'waiting for connections on port' $logfile
while [[ $? -ne 0 && $COUNTER -lt 10 ]] ; do
    sleep 1
    let COUNTER+=1
    grep -q 'waiting for connections on port' $logfile
done

mongo < nodegoat_db_reset.js
#cd /var/www | grunt run
PORT=8888 nodejs /var/www/server.js
