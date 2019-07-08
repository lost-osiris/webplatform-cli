FROM docker.io/fedora:24
MAINTAINER Matthew Owens mowens@redhat.com

RUN dnf groupinstall -y "Development Tools"

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
   procps

WORKDIR /home/container

RUN pip3.5 install --upgrade pip

ADD main_requirements.txt /home/container/
RUN pip3.5 install -r main_requirements.txt

ADD deps_requirements.txt /home/container/
RUN pip3.5 install -r deps_requirements.txt

RUN setcap cap_net_raw,cap_net_admin+p /usr/bin/ping

VOLUME "/home/container/config/"
VOLUME "/home/container/actions/"
VOLUME "/home/cee-tools/setup/"
VOLUME "/home/cee-tools/logs/"

VOLUME "/home/cee-tools/frontend/"

EXPOSE 8000

#RUN dnf install -y sudo

#RUN useradd -ms /bin/bash mowens && echo "docker:docker" | chpasswd && adduser docker sudo

#USER mowens
ADD entry.sh /home/container/
ENTRYPOINT /home/container/entry.sh

