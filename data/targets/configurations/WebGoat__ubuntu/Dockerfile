FROM ubuntu:raring
MAINTAINER stanislav

RUN apt-get update
RUN mkdir /var/www/

RUN mkdir /var/www/webgoat
ADD . /var/www/webgoat/

EXPOSE 80

CMD cd /var/www/webgoat/ && sh webgoat.sh start80




