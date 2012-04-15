
pythonz: a Python installation manager
======================================

Overview
--------

pythonz is a program to automate the building and installation of Python in the users $HOME. This is
a fork of the original project, `pythonbrew <https://github.com/utahta/pythonbrew>`_.

The original project seems to be unmaintained, and it also has some extra features which I don't really
need, so I made this for to make something a bit simpler that works for *me*. Yoy may also find it
useful.

CPython, Stackless and PyPy are supported.

Installation
------------

The recommended way to download and install pythonz is to run these statements in your shell::

  curl -kL https://raw.github.com/saghul/pythonz/master/pythonz-install | bash

or::

  fetch -o - https://raw.github.com/saghul/pythonz/master/pythonz-install | bash

After that, pythonz installs itself to ~/.pythonz.

Please add the following line to the end of your ~/.bashrc::

  [[ -s $HOME/.pythonz/etc/bashrc ]] && source $HOME/.pythonz/etc/bashrc

If you need to install pythonz into somewhere else, you can do that by setting a PYTHONZ_ROOT environment variable::

  export PYTHONZ_ROOT=/path/to/pythonz
  curl -kLO https://raw.github.com/saghul/pythonz/master/pythonz-install
  chmod +x pythonz-install
  ./pythonz-install

For Systemwide(Multi-User) installation
---------------------------------------

If the install script is run as root, pythonz will automatically install into /usr/local/pythonz.

pythonz will be automatically configured for every user on the system if you install it as root.

After installing it, where you would normally use `sudo`, non-root users will need to use `sudo-pythonz`::

  sudo-pythonz install 2.7.2

Usage
-----

pythonz command [options] version

Install some pythons::

  pythonz install 2.7.2
  pythonz install -t stackless 2.7.2
  pythonz install -t pypy --url https://bitbucket.org/pypy/pypy/downloads/pypy-1.8-osx64.tar.bz2 1.8
  pythonz install --verbose 2.7.2
  pythonz install --configure="CC=gcc_4.1" 2.7.2
  pythonz install --url http://www.python.org/ftp/python/2.7/Python-2.7.2.tgz 2.7.2
  pythonz install --file /path/to/Python-2.7.2.tgz 2.7.2
  pythonz install 2.7.2 3.2

Use the specified python in current shell::

  pythonz use 2.7.2

List the installed pythons::

  pythonz list

List all the available python versions for installing::

  pythonz list -a

Uninstall the specified python::

  pythonz uninstall 2.7.2
  pythonz uninstall -t stackless 3.2.2

Remove stale source folders and archives::

  pythonz cleanup

Upgrades pythonz to the latest version::

  pythonz update

Disable pythonz in the current shell::

  pythonz off

Commands
--------

See the available commands::

  pythonz help

To get help on each individual command run::

  pythonz help <command>


