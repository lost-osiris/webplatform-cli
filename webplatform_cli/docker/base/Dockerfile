FROM docker.io/fedora:24
LABEL maintainer="Matthew Owens mowens@redhat.com"

WORKDIR /home/root

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
RUN pip3 install --upgrade pip
ADD requirements.txt /home/container/
RUN pip3 install -r /home/container/requirements.txt

# Mongodb Setup
RUN groupadd -r mongodb && useradd -r -d /home/mongodb/ -g  mongodb mongodb
RUN usermod mongodb -a -G wheel

# Platform Setup
ADD platform-requirements.txt /home/container/
RUN pip3 install -r /home/container/platform-requirements.txt

# ADD entry.sh /home/container/

VOLUME "/home/container/config/"
VOLUME "/home/container/actions/"
VOLUME "/home/container/data/"
VOLUME "/home/container/service/"
VOLUME "/home/container/webplatform_cli/"

WORKDIR /home/container


# RUN export PYTHONPATH="${PYTHONPATH}:/home/container/webplatform_cli"
# RUN export PATH="${PATH}:/home/container/webplatform_cli"