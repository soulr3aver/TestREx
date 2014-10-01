#!/bin/sh
docker kill `docker ps -notrunc -a -q`
docker rm `docker ps -notrunc -a -q`
docker rmi -f $(docker images -a | grep "^<none>" | awk '{print $3}')
