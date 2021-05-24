FROM ubuntu:20.04 AS front

ENV TZ=Europe/Moscow
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt install nodejs npm -y && \
    npm install -g npm@7.11.2

ADD frontend/package.json /tmp/package.json
RUN cd /tmp && npm install --legacy-peer-deps

ADD frontend /frontend

RUN cd /frontend/ && \
    cp -a /tmp/node_modules . && \
    export NG_CLI_ANALYTICS=ci && \
    npm run-script build



FROM ubuntu:20.04

LABEL maintainer='stepanenko <stepanenko@selectel.ru>'

RUN apt-get update

RUN apt-get install python3 python3-dev python3-pip libev-dev locales -y
RUN pip3 install flask bjoern sqlalchemy sqlalchemy_utils pymysql pytest

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=Europe/Moscow
ENV DEBIAN_FRONTEND=noninteractive

RUN apt install -y nginx


COPY --from=front /frontend/dist/workshop/ /front

ADD . /app

ADD nginx/nginx.conf /etc/nginx/sites-enabled/default

STOPSIGNAL SIGTERM

RUN chmod +x /app/run.sh
RUN cp /app/nginx/nginx.conf /etc/nginx/sites-enabled/default

ENTRYPOINT ["/app/run.sh"]
