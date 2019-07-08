#!/bin/bash -x
echo "$HOST_MACHINE     host-machine" >> /etc/hosts
#sh /home/container/actions/ssl.sh
sh /home/container/actions/start.sh
tail -f /home/cee-tools/logs/error.log
