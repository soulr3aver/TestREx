FROM testbed/ubuntu-node-mongo
MAINTAINER danielrs

ADD . /var/www

RUN cd /var/www ; npm install -d

RUN chmod +x /var/www/run.sh
CMD cd /var/www && ./run.sh
