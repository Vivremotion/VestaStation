FROM arm32v7/alpine:latest

RUN apk add bluez \
    && apk add bluez-dev \
    && apk add rng-tools \
    && apk add gcc \
    && apk add musl-dev \
    && apk add python3-dev build-base \
    && python3 -m ensurepip \
    && pip3 install -U pip \
    && pip3 install --upgrade setuptools pybluez firebase-admin

RUN pip3 install Adafruit_DHT

COPY . ./usr/share/Station

ENTRYPOINT python3 ./usr/share/Station/Initialize.py
