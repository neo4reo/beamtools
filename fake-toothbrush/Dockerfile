FROM debian:jessie

MAINTAINER @cryptax

# docker run -it --net=host --privileged --name fake-toothbrush cryptax/bleno /bin/bash

# Install bleno and dependencies ---------------
# bluetooth IS required despite we do service bluetooth stop in the end
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -yqq \
    wget \
    curl \
    build-essential \
    bluetooth \
    bluez \
    emacs \
    locate \
    libbluetooth-dev \
    libudev-dev \
    usbutils \
    && rm -rf /var/lib/apt/lists/*		   

RUN curl -sL https://deb.nodesource.com/setup_7.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && npm install bleno 

WORKDIR /root

# Cleaning up and final setup -------------------------
RUN apt-get autoremove -yqq
RUN apt-get clean

RUN service bluetooth stop





