FROM ubuntu:14.04

MAINTAINER stasevseev@gmail.com

RUN apt-get update -y
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:chris-lea/nginx-devel -y

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get install -y python2.7 python-setuptools nginx supervisor git build-essential gcc libxml2-dev libxslt1-dev \
    libpq-dev python2.7-dev postgresql-9.3 libjpeg-dev redis-server postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
RUN easy_install pip

WORKDIR /var/local/www/
RUN git clone https://github.com/StasEvseev/adminbuy.git
WORKDIR /var/local/www/adminbuy
RUN pip install -r REQUIREMENTS

RUN /etc/init.d/postgresql start &&\
    sudo -u postgres psql -c "CREATE ROLE adminbuy WITH PASSWORD 'adminbuy' NOSUPERUSER CREATEDB NOCREATEROLE LOGIN;" &&\
    sudo -u postgres psql -c "CREATE DATABASE adminbuy WITH OWNER=adminbuy TEMPLATE=template0 ENCODING='utf-8';" &&\
    /etc/init.d/postgresql stop


# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

RUN /etc/init.d/postgresql start && python manage.py db upgrade && python manage.py create_superuser

# Nginx
COPY config/buyapi /etc/nginx/sites-enabled
COPY certs/ssl.crt /etc/nginx/ssl.crt
COPY certs/private.key /etc/nginx/private.key
RUN ln -s /etc/nginx/sites-enabled/buyapi /etc/nginx/sites-available/buyapi

RUN /etc/init.d/nginx start

# Supervisor
COPY config/supervisor/buyapi.conf /etc/supervisor/conf.d/buyapi.conf

RUN /etc/init.d/nginx restart && service supervisor start && supervisorctl reread && supervisorctl reload

EXPOSE 443
EXPOSE 80

COPY start.sh /var/local/www/adminbuy/start.sh
RUN chmod +x /var/local/www/adminbuy/start.sh

CMD ["/var/local/www/adminbuy/start.sh"]