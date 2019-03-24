import subprocess, os, sys, pwd

def run(settings, params):
   env = settings.get_environ_set(environ=os.environ.copy())
   config = settings.get_config('ctl')
   
   env['username'] = os.getenv("LOGNAME")
  
   # log_path = config['app-root'] + "/logs/install.log"
   # log = open(log_path, "w+")
   path = config['scripts-path'] + "/" + config['install']
   
   install = subprocess.Popen(" ".join(["sh", path]), shell=True, env=env, stdout=log, executable="/bin/bash")
   try:
      install.communicate()
      install.wait()
   except KeyboardInterrupt:
      install.kill()
      print("\n")
   
   sys.exit()
