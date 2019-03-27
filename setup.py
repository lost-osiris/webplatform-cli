# from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "webplatform-cli",
   version = "1.0.11",
   description = "CLI used for a webplatform",
   author = "Matthew Owens",
   author_email = "mowens@redhat.com",
   url = "https://github.com/lost-osiris/webplatform-cli",
   # packages = ['lib', 'controller'],
   packages = find_packages(exclude=("db", "settings")),
   # package_data={
   #    '': [
   #       'settings/*',
   #       'db/docker/*',
   #       'db/data/README.md'
   #    ]
   # },
   include_package_data = True,
   install_requires = [
      'docker',
      'pymongo'
   ],
   license='MIT',
   scripts = ["webplatform_cli/webplatform-cli"],
   long_description = """TODO""",
   classifiers = [
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
