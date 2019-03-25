#!/usr/bin/python3 -B
   # service-ctl [ --force --debug] <instance> <command> [<args>...]
   # service-ctl [ --force --debug] <command> [<args>...]
   # service-ctl [ --force --debug] <command> [<args>...]
"""usage:
   webplatform-cli [ --force --debug ] <command> [<args>...]
   webplatform-cli (--version | --help)

options:
   -h --help                            Print this help message
   --version                            Show version
   -f --force                           Force the action being preformed
   -d --debug                           Enable controller debugging mode,
                                        for controller development only

commands for the controller are:
   setup        Build containters
   update       *not finished* Local dependancy update
   start        Start
   stop         Stop
   restart      Restart

See 'webplatform-cli <command> -h' for more information on a specific command.
"""
import os
import sys

sys.dont_write_bytecode = True

cmd = {
   'setup':{'type':'noargs','headless':False},
   'start':{'type':'service','headless':True},
   'restart':{'type':'service','headless':True},
   'stop':{'type':'service','headless':True},
}

controller_path = os.path.dirname(os.path.realpath(__file__))
virtv_path = controller_path + '/virtv/lib/'

base_path = os.path.abspath(os.path.join(controller_path, '..'))
app_path = base_path + '/api'
python_version = os.listdir(virtv_path)

deps_path = virtv_path + "/%s/site-packages/" % python_version

if app_path not in sys.path:
   sys.path.append(app_path)

if controller_path not in sys.path:
   sys.path.append(controller_path)

if deps_path not in sys.path:
   sys.path.append(deps_path)

from dependencies.docopt import docopt
from ctl import Docker
from lib.utils.config import Settings

import json

if __name__ == "__main__":
   import docker
   args = docopt(__doc__,
               version='Web Platform CLI Version 1.0',
               options_first=True)

   if not args['<command>'] in list(cmd.keys()):
      sys.stderr.write(__doc__)
      sys.exit(1)

   instance = args['--instance']
   verify = not cmd[args['<command>']]['headless']

   settings = Settings(base_path, verify=verify, instance=instance)

   import commands_parser as parser
   subargs = getattr(parser, 'docopt_%s' % (cmd[args['<command>']]['type'],))(args['<command>'], args['<args>'])

   ctrl = {}

   if cmd[args['<command>']]['type'] == 'noargs':
      ctrl['params'] = []
   elif cmd[args['<command>']]['type'] == 'run':
      ctrl['params'] = []
      for i in args['<args>']:
         if i != "run":
            ctrl['params'].append(i)
   else:
      ctrl['params'] = subargs['<args>']

   ctrl['command'] = args['<command>']

   controller = Docker(settings, debug=args['--debug'], force=args['--force'])
   controller.parse_args(**ctrl)
