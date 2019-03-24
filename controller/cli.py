from handler import ContainerHandler
import os, docker

class Docker(object):
   def __init__(self, settings, debug, force):
      self.settings = settings
      self.config = self.settings.get_config("ctl")
      self.debug = debug
      self.force = force

      self.options = {
         "debug": self.debug,
         "force": self.force,
      }

      self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
      self.services = self.settings.get_service()
      self.instance = settings.get_instance()
      self.base_path = settings.get_path()

   def parse_args(self, **kwargs):
      #only run setup and install, others have yet to be implemented
      if kwargs['command'] in ["build", "install"]:
         getattr(self, "%s" % (kwargs['command'], ), None)(kwargs['params'])

      elif kwargs['command'] in ["start", "restart", "stop", "update", "reset"]:

         if len(kwargs['params']) > 0:
            for i in kwargs['params']:
               self.run_container(service=i, action=kwargs['command'])
         else:
            self.run_container(action=kwargs['command'])

      elif kwargs['command'] == "tail":
         self.tail(kwargs['params']['service'], follow=kwargs['params']['follow'])

   def run_container(self, service=None, action=None):
      container = ContainerHandler(self.settings, self.client, self.options)
      if service == None:
         container.run(action)
      else:
         container.run_service(service, action)

   def build(self, params):
      from tasks import build

      force = self.options['force']

      if len(params) == 0:
         for service in self.services:
            docker_file = "%s/setup/instances/%s/%s/" % (self.base_path, self.instance, service)

            base = "%s/setup/docker/%s/" % (self.base_path, service)
            if not os.path.exists(base):
               base = False

            build.run(service, docker_file, force=force, base=base)
      else:
         for service in params:
            services = self.settings.get_service(service=service)

            base = "%s/setup/docker/%s/" % (self.base_path, service)
            if not os.path.exists(base):
               base = False

            if type(services) is list:
               for i in services:
                  node = "%s_%s" % (service, i)
                  docker_file = "%s/setup/instances/%s/%s/" % (self.base_path, self.instance, node)

                  build.run(node, docker_file, force=force, base=base)
            else:
               docker_file = "%s/setup/instances/%s/%s/" % (self.base_path, self.instance, service)
               build.run(service, docker_file, force=force, base=base)

   def install(self, params):
      from tasks import install
      install.run(self.settings, params)

   def tail(self, services, follow=False):
      container = ContainerHandler(self.settings, self.client, self.options)
      container.tail(services[0], follow=follow)
