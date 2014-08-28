FROM testbed/ubuntu-node-mongo
MAINTAINER standash

ADD . /var/www

RUN cd /var/www ; npm install -d
RUN npm install -g grunt-cli
RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN chmod +x /var/www/run.sh
CMD cd /var/www && ./run.sh
