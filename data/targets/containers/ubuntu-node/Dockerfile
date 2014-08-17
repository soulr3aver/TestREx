FROM ubuntu:lucid
MAINTAINER danielrs

RUN mkdir -p /data/db

RUN apt-get update
RUN apt-get -y install nodejs
RUN apt-get -y install npm

EXPOSE 8888

CMD ["nodejs"]

