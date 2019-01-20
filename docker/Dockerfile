FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python2.7 python-setuptools supervisor git build-essential gcc libxml2-dev libxslt1-dev \
    libpq-dev python2.7-dev libjpeg-dev

RUN easy_install pip

RUN mkdir /code
WORKDIR /code
ADD REQUIREMENTS /code/
RUN pip install -r REQUIREMENTS
ADD . /code/
RUN python manage.py assets build || true

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
