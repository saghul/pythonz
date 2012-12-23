
import os
from distutils.core import setup


def find_packages(toplevel):
    return [directory.replace(os.path.sep, '.') for directory, subdirs, files in os.walk(toplevel) if '__init__.py' in files]

setup(name='pythonz',
      version              = 'dev',
      description          = 'Manage python installations in your system',
      long_description     = open('README.rst').read(),
      author               = 'utahta',
      author_email         = 'labs.ninxit@gmail.com',
      maintainer           = 'saghul',
      maintainer_email     = 'saghul@gmail.com',
      url                  = 'https://github.com/saghul/pythonz',
      license              = 'MIT',
      packages             = find_packages('pythonz'),
      include_package_data = True,
      entry_points         = dict(console_scripts=['pythonz_install=pythonz.installer:install_pythonz']),
      zip_safe             = False,
      classifiers          = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
      ])

