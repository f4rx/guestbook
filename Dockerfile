FROM ubuntu

MAINTAINER nortlite <zubov@selectel.ru>

RUN apt-get update && apt-get install python3-pip libev-dev locales -y
RUN pip3 install flask bjoern sqlalchemy sqlalchemy_utils pymysql pytest
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . /app

ENTRYPOINT ["/usr/bin/python3", "/app"]