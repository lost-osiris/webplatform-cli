#!/usr/bin/python3 -B
   # service-ctl [ --force --debug] <instance> <command> [<args>...]
   # service-ctl [ --force --debug] <command> [<args>...]
   # service-ctl [ --force --debug] <command> [<args>...]
"""usage:
   service-ctl [ --force --debug --instance INSTANCE] <command> [<args>...]
   service-ctl (--version | --help)

options:
   -h --help                            Print this help message
   --version                            Show version
   -f --force                           Force the action being preformed
   -i INSTANCE --instance=INSTANCE      Specify Instance [default: devel]
   -d --debug                           Enable controller debugging mode,
                                        for controller development only

commands for the controller are:
   build        Build containters
   install      *not finished* Global dependancy install, requires root
   update       *not finished* Local dependancy update
   start        Start  container
   stop         Stop container
   restart      Restart container
   reset   Removes container then starts it again
   tail         *not finished* Watch log files for services

See 'ceetools-ctl <command> -h' for more information on a specific command.
"""
import os
import sys

sys.dont_write_bytecode = True

cmd = {
   'start':{'type':'service','headless':False},
   'stop':{'type':'service','headless':False},
   'restart':{'type':'service','headless':False},
   'reset':{'type':'service','headless':False},
   'update':{'type':'service','headless':False},
   'install':{'type':'noargs','headless':True},
   'build':{'type':'build','headless':False},
   'tail':{'type':'tail','headless':False},
   'run':{'type':'run','headless':False},
   'exec':{'type':'exec','headless':False},
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
               version='CEE-Tools Controller Version 1.0',
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
