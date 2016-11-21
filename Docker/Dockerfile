FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get install software-properties-common
RUN add-apt-repository ppa:chris-lea/nginx-devel -y
RUN apt-get install -y python2.7 python-setuptools nginx supervisor git build-essential gcc libxml2-dev libxslt1-dev libpq-dev python2.7-dev postgresql-9.3 libjpeg-dev redis-server
RUN easy_install pip
RUN mkdir -p /var/local/www/
WORKDIR /var/local/www/
RUN git clone https://github.com/StasEvseev/adminbuy.git
WORKDIR /var/local/www/adminbuy
RUN pip install -r REQUIREMENTS
RUN service postgresql start
RUN sudo -u postgres psql -c "CREATE ROLE adminbuy WITH PASSWORD 'adminbuy' NOSUPERUSER CREATEDB NOCREATEROLE LOGIN;"
RUN sudo -u postgres psql -c "CREATE DATABASE adminbuy WITH OWNER=adminbuy TEMPLATE=template0 ENCODING='utf-8';"
RUN python manage.py db upgrade
