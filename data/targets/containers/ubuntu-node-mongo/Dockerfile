FROM ubuntu:13.10
MAINTAINER danielrs

RUN mkdir -p /data/db

RUN apt-get update
RUN apt-get -y install nodejs
RUN apt-get -y install npm
RUN apt-get -y install mongodb

EXPOSE 8888 27017

CMD ["mongod"]
