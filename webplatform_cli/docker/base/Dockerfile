FROM docker.io/fedora:24
LABEL maintainer="Matthew Owens mowens@redhat.com"

ADD mongodb-org-3.2.repo /etc/yum.repos.d/

RUN dnf groupinstall -y "Development Tools"
RUN dnf -y install mongodb-org
RUN dnf install -y \
   wget \
   tar \
   gcc \
   openssl openssl-devel \
   redhat-rpm-config \
   mod_ssl \
   python-devel \
   mysql mysql-devel \
   xmlsec1 xmlsec1-devel \
   xmlsec1-openssl xmlsec1-openssl-devel \
   libtool-ltdl-devel \
   python-pip \
   mod_wsgi \
   python3-devel \
   npm \
   iputils \
   which \
   nginx \
   procps \
   git \
   openssl \ 
   openssl-devel \
   numactl 

RUN setcap cap_net_raw,cap_net_admin+p /usr/bin/ping

# Flask Setup
RUN pip3.5 install --upgrade pip

ADD requirements.txt /home/container/
RUN pip3.5 install -r requirements.txt

# Mongodb Setup
# RUN groupadd -r mongodb && useradd -r -d /home/mongodb/ -g  mongodb mongodb
# RUN chown -R mongodb:mongodb /data
# RUN mkdir -p /data/db /data/configdb
# RUN chown -R mongodb:mongodb /data/db /data/configdb
# RUN usermod mongodb -a -G wheel

WORKDIR /home/container

VOLUME "/home/container/config/"
VOLUME "/home/container/actions/"
VOLUME "/home/container/data/"