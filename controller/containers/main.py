from lib.utils.config import Settings
import socket

settings = Settings()
base_path = settings.get_path()
instance = settings.get_instance()

volumes = {
   # "%s/application" % base_path: {
   #    "bind": "/home/cee-tools/setup",
   #    "mode": "rw",
   # },
   # "%s/setup/instances/" % base_path: {
   #    "bind": "/home/cee-tools/setup",
   #    "mode": "rw",
   # },
}

def add_volumes(add):
   tmp = volumes
   for key, value in add.items():
      tmp[key] = value
   return tmp

def get_environment(service):
   return {
      "HOST_MACHINE": socket.gethostbyname(socket.gethostname()),
      "CEE_TOOLS_INSTANCE": instance,
      "CEE_TOOLS_SERVICE": service,
   }
