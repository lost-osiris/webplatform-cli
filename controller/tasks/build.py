from lib.utils.config import Settings
from docker import APIClient
import os

settings = Settings()
instance = settings.get_instance()
client = APIClient(base_url="unix://var/run/docker.sock")

def build_base(service, path, force):
   name = "cee-tools-base-%s" % service
   image_name = 'cee-tools-base-%s:latest' % (service)

   print("Building base image for (%s)." % service)
   kwargs = {
      'decode': True,
      # 'nocache': force,
      'forcerm': True,
      'path': path,
      'rm': True,
      'tag': image_name,
      'stream': True,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image for (%s)." % service)

def run(service, path, force=False, base=True):
   image_name = 'cee-tools-%s-%s:latest' % (instance, service)

   if base:
      build_base(service.split("_")[0], base, force)

   dockerfile = path + 'Dockerfile'
   context = os.path.abspath(os.path.join(path, '..', '..', 'common', service))

   print("Building (%s) image." % service)
   kwargs = {
      'nocache': force,
      'decode': True,
      'forcerm': True,
      'path': context,
      'dockerfile': dockerfile,
      'rm': True,
      'tag': image_name,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image for (%s)." % service)
