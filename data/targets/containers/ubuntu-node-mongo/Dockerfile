FROM testbed/ubuntu-node
MAINTAINER danielrs

RUN mkdir -p /data/db

RUN apt-get update
RUN apt-get -y install mongodb

EXPOSE 27017

CMD ["mongod"]
