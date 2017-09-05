# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=dockerfile

FROM alpine:latest

ARG APP_UID=${APP_UID:-1000}
ENV APP_UID=${APP_UID}

RUN apk add --update --no-cache \
        curl \
        ca-certificates \
        pcre \
        python3 \
        shadow \
&&  curl -# -L https://bootstrap.pypa.io/get-pip.py | python3 - \
&&  apk add --update --no-cache --virtual .uwsgi \
        gcc \
        gzip \
        linux-headers \
        musl-dev \
        pcre-dev \
        python3-dev \
        tar \
&&  CPUCOUNT=1 pip3 install uwsgi virtualenv \
&&  apk del .uwsgi \
&&  mkdir -p -m0773 /var/run/venv \
&&  mkdir -p -m0773 /var/log/uwsgi \
&&  mkdir -p -m0773 /var/run/uwsgi

CMD ["uwsgi", "--ini=/etc/uwsgi/uwsgi.ini"]
