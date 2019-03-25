#FROM mongo:latest
FROM docker.io/fedora:24
MAINTAINER Matthew Owens mowens@redhat.com

EXPOSE 27017

RUN groupadd -r mongodb && useradd -r -d /home/mongodb/ -g  mongodb mongodb
RUN usermod mongodb -a -G wheel

ADD mongodb-org-3.2.repo /etc/yum.repos.d/
RUN dnf -y install mongodb-org iputils  git openssl openssl-devel procps numctl

RUN setcap cap_net_raw,cap_net_admin+p /usr/bin/ping

WORKDIR /home/container

RUN mkdir /home/container/daemon/

VOLUME "/data/db/"
VOLUME "/home/container/config/"

RUN chown -R mongodb:mongodb /data

RUN mkdir -p /home/cee-tools/mongodb

RUN mkdir -p /data/db /data/configdb
RUN chown -R mongodb:mongodb /data/db /data/configdb

ADD entry.sh /home/container/
CMD /home/container/entry.sh
