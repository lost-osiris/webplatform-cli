import os, sys, docker, json, shutil

class CLI(object):
   def __init__(self, settings, debug, force):
      self.settings = settings
      # self.config = self.settings.get_config("cli")
      self.debug = debug
      self.force = force

      self.options = {
         "debug": self.debug,
         "force": self.force,
      }

      self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
      self.services = self.settings.get_service()
      self.base_path = settings.get_path()

   def parse_args(self, command, params):
      #only run setup and install, others have yet to be implemented 
      if command == "setup":
         method = getattr(self, command, None)()
     
      elif command == "config":
         method = getattr(self, command, None)(**params)
      
      elif command == "variables":
         self.parse_variables(**params)
      
      elif command == "apps":
         self.parse_apps(**params)
     
      elif command in ["start", "restart", "stop", "update", "reset"]:
         if len(params) > 0:
            for i in params:
               self.run_container(service=i, action=command)
         else:
            self.run_container(action=command)

   def run_container(self, service=None, action=None):
      from Docker import ContainerHandler
      
      container = ContainerHandler(self.settings, self.client, self.options)
      if service == None:
         container.run(action)
      else:
         container.run_service(service, action)

   def config(self, command, service, path=None, config=None, default=False):
      if command in "get":
         config = self.settings.get_config(service)
         print(json.dumps(config, indent=2))
         sys.exit(1)
         
      
      try:
         if not default:
            if config == None:
               config = json.load(open(path))

      except IsADirectoryError:
         print("The value you specified for '--config' is a directory. This value but be a JSON file")
      except TypeError as e:
         print("The config you specified is not valid JSON")
      finally:
         config_path = "%s/settings/%s.json" % (self.base_path, service)
         default_path = "%s/settings/default-%s.json" % (self.base_path, service)
         
         config_target = open(config_path, "w")

         if not os.path.isfile(default_path):
            default_target = open(default_path, "w+")
            default_target.write(json.dumps(self.settings.get_config(service), indent=2))

         if not default:
            config_target.write(json.dumps(config, indent=2))
         else:
            config = json.load(open(default_path))
            config_target.write(json.dumps(config, indent=2))

      # print(command, service, path)
   def parse_variables(self, command=None, variable=None, value=None, default=False):
      config = self.settings.get_config("variables")

      current_value = self.settings.get_variable(variable)
      if current_value == None:
         sys.exit(1)

      if command == "get":
         print(current_value)
         sys.exit(1)

      if not default:
         if "," in value:
            config[variable] = value.strip().split(",")
         else:
            config[variable] = value

      self.config("set", "variables", config=config, default=default)
   
   def parse_apps(self, command=None, app=None, default=False):
      config = self.settings.get_config("variables")

      current_value = self.settings.get_variable("applications")

   def setup(self):
      from tasks import build

      build.run("mongodb", force=self.options['force'])

   def tail(self, service, follow=False):
      pass