FROM testbed/ubuntu-apache-mysql
MAINTAINER danielrs

RUN mkdir /var/www/wordpress

ADD . /var/www/wordpress

RUN chmod +x /var/www/wordpress/run.sh
CMD cd /var/www/wordpress && ./run.sh
