FROM ubuntu:13.10
MAINTAINER danielrs

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-client mysql-server apache2 libapache2-mod-php5 php5-mysql php5-ldap
RUN chown -R www-data:www-data /var/www/

EXPOSE 80 3306

CMD ["mysqld"]
