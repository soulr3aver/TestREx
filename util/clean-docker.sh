#!/bin/sh
docker kill `docker ps -notrunc -a -q`
docker rm `docker ps -notrunc -a -q`
chmod 777 /var/run/docker.sock
docker rmi -f $(docker images -a | grep "^<none>" | awk '{print $3}')
