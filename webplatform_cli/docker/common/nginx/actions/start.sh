#!/bin/bash -x
if [ ! -e "/run/nginx.pid" ]; then
  echo "Starting '$CEE_TOOLS_SERVICE' on instance '$CEE_TOOLS_INSTANCE'"
  nginx -c /home/container/config/nginx.conf
else
  echo "Already running '$CEE_TOOLS_SERVICE' on instance '$CEE_TOOLS_INSTANCE'"
fi
