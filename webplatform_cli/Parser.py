from lib.config import Settings
from docopt import docopt
import os, sys

settings = Settings()
config = settings.get_config("cli")
services = settings.get_config("cli")['services']

def docopt_config(command, argv):
   valid_args = sorted(services + ["cli"])
   args_doc = '\n   '.join(valid_args)
   doc = """usage: 
   webplatform-cli <command> <service> --path <path>
   webplatform-cli <command> <service> --default
   webplatform-cli <command> [<service>]

commands allowed on config (all commands a service must be specified)
   set       Set the config file to be used for a given service.
             The --config argument is required.
             You can also specify --default to reset all the config files

   get       Get the data in specified service config

the following are valid services with configs:
   %s
""" % args_doc
   
   args = docopt(doc, argv=argv)

   if args['<command>'] == 'set' and not args['--path'] and not args['--default']:
      sys.stderr.write(doc)
      sys.exit(1)

   # if args['--config']:
   #    args['<config>'] = os.path.abspath(os.path.join(settings.get_path(), args['<config>']))
   
   return args

def docopt_service(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(sorted(valid_args))
   doc = """usage:
   webplatform-ctl [options] %s [<args>...]

options:
   -h --help     Print this help message

%s the following processies:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)
   if valid_args.issuperset(args['<args>']):
      return args
   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_build(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(valid_args)
   doc = """usage:
   webplatform-ctl [options] %s [<args>...]

options:
   -h --help     Print this help message

%s the following processies with the controller:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)
   if valid_args.issuperset(args['<args>']):
      return args
   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_tail(command, argv):
   argv.insert(0, command)
   valid_args = set(services)
   args_doc = '\n   '.join(valid_args)
   doc = """usage:
   webplatform-ctl [options] %s [--follow] [<args>...]

options:
   -h --help     Print this help message
   -F --follow   Stream output from container

%s the following processies with the controller:
   %s
""" % (command, command, args_doc)

   args = docopt(doc, argv=argv)

   if args['--follow']:
      args['<args>'] = {'follow': True, 'service': args['<args>']}
      return args

   elif valid_args.issuperset(args['<args>']):
      args['<args>'] = {'follow': False, 'service': args['<args>']}
      return args

   else:
      sys.stderr.write(doc)
      sys.exit(1)

def docopt_noargs(command, argv):
   argv.insert(0,command)
   doc = """usage:
   webplatform-ctl [options] %s

options:
   -h --help     Print this help message
""" % (command,)
   return docopt(doc,argv=argv)

def docopt_run(command, argv):
   argv.insert(0,command)
   doc = """usage:
   webplatform-ctl [options] %s <script>...

options:
   -h --help     Print this help message
""" % (command,)

   return docopt(doc, argv=argv)
