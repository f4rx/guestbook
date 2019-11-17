FROM ubuntu:18.04 AS front

RUN apt-get update && \
    apt install -y xz-utils wget && \
    mkdir -p /usr/local/lib/nodejs
RUN wget https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-x64.tar.xz && \
    tar -xJvf node-v12.13.0-linux-x64.tar.xz -C /usr/local/lib/nodejs
RUN export PATH=/usr/local/lib/nodejs/node-v12.13.0-linux-x64/bin:$PATH && \
    export NG_CLI_ANALYTICS=ci && \
    npm install -g @angular/cli && \
    npm install @angular-devkit/build-angular && \
    npm install -S @carbon/icons-angular

ADD frontend /frontend

RUN export PATH=/usr/local/lib/nodejs/node-v12.13.0-linux-x64/bin:$PATH && \
    export NG_CLI_ANALYTICS=ci && \
    cd /frontend/ && \
    npm install && \
    ng build


FROM ubuntu:18.04
COPY --from=front /frontend/dist/workshop/ /front

LABEL maintainer='nortlite <zubov@selectel.ru>'

RUN apt-get update && apt-get install python3-pip libev-dev locales -y
RUN pip3 install flask bjoern sqlalchemy sqlalchemy_utils pymysql pytest
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt install -y nginx

ADD . /app

RUN chmod +x /app/run.sh
RUN cp /app/nginx/nginx.conf /etc/nginx/sites-enabled/default

ENTRYPOINT ["/app/run.sh"]
