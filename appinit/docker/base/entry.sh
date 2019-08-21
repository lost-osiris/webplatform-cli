#!/bin/bash
# PYTHONPATH=/home/container/cli:$PYTHONPATH
# PYTHON=/home/container/cli:$PATH
export PYTHONPATH=$PYTHONPATH:/home/container/appinit
export PATH=$PATH:/home/container/appinit

. /home/container/actions/entry.sh