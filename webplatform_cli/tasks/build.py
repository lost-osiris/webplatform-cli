from docker import APIClient
import os, webplatform_cli

client = APIClient(base_url="unix://var/run/docker.sock")

def run(service, force=False):
   path = os.path.dirname(webplatform_cli.__file__)
   
   image_name = 'webplatform-base:latest'

   print("Building base image.")
   kwargs = {
      'nocache': force,
      'decode': True,
      'forcerm': True,
      'path': path + "/docker/base/",
      'dockerfile': path + "/docker/base/Dockerfile",
      'rm': True,
      'tag': image_name,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image.")
