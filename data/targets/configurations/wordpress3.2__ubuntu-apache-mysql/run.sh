#!/bin/bash
mysqld_safe &
sleep 5
mysql < database.sql

mysqladmin -u root password toor

apache2ctl start

#the container must keep running :)
while :;
do
:;
done
