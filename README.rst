pythonz: a Python installation manager
======================================

Overview
--------

pythonz is a program to automate the building and installation of Python in the users $HOME. This is
a fork of the original project, `pythonbrew <https://github.com/utahta/pythonbrew>`_.

The original project seems to be unmaintained, and it also has some extra features which I don't really
need, so I made this for to make something a bit simpler that works for *me*. You may also find it
useful.

CPython, Stackless, PyPy and Jython are supported.

Installation
------------

The recommended way to download and install pythonz is to run these statements in your shell::

  curl -kL https://raw.github.com/saghul/pythonz/master/pythonz-install | bash

or::

  fetch -o - https://raw.github.com/saghul/pythonz/master/pythonz-install | bash

After that, pythonz installs itself to ``~/.pythonz``.

Please add the following line to the end of your ``~/.bashrc``::

  [[ -s $HOME/.pythonz/etc/bashrc ]] && source $HOME/.pythonz/etc/bashrc

If you need to install pythonz into somewhere else, you can do that by setting a ``PYTHONZ_ROOT`` environment variable::

  export PYTHONZ_ROOT=/path/to/pythonz
  curl -kLO https://raw.github.com/saghul/pythonz/master/pythonz-install
  chmod +x pythonz-install
  ./pythonz-install

For Systemwide (Multi-User) installation
---------------------------------------

If the install script is run as root, pythonz will automatically install into ``/usr/local/pythonz``.

pythonz will be automatically configured for every user on the system if you install it as root.

After installing it, where you would normally use `sudo`, non-root users will need to use `sudo-pythonz`::

  sudo-pythonz install 2.7.3

Usage
-----

::

  pythonz command [options] version

Before building Python, you might want to install some optional dependencies, for functionality that
is often expected to be included in a Python build (it can be a bummer to discover these missing and
have to rebuild your python setup). These include the following, ordered by (very roughly guessed)
probability that you will need them (names may differ in your system package manager)::

  libz-dev (or zlib)
  libbz2-dev
  libreadline-dev
  libsqlite3-dev
  libncurses5-dev
  libgdbm-dev

Install some pythons::

  pythonz install 2.7.3
  pythonz install -t stackless 2.7.2
  pythonz install -t jython 2.5.2
  pythonz install -t pypy --url https://bitbucket.org/pypy/pypy/downloads/pypy-1.8-osx64.tar.bz2 1.8
  pythonz install --verbose 2.7.2
  pythonz install --configure="CC=gcc_4.1" 2.7.2
  pythonz install --url http://www.python.org/ftp/python/2.7/Python-2.7.2.tgz 2.7.2
  pythonz install --file /path/to/Python-2.7.2.tgz 2.7.2
  pythonz install 2.7.3 3.2.3

List the installed pythons::

  pythonz list

List all the available python versions for installing::

  pythonz list -a

Uninstall the specified python::

  pythonz uninstall 2.7.3
  pythonz uninstall -t stackless 3.2.2

Remove stale source folders and archives::

  pythonz cleanup

Upgrade pythonz to the latest version::

  pythonz update

Upgrade pythonz to the latest development version::

  pythonz update --dev

Check the installed pythonz version::

  pythonz version

The recommended way to use a pythonz-installed version of Python is through `virtualenv`, e.g.::

  mkvirtualenv -p ~/.pythonz/pythons/CPython-2.7.3/bin/python python2.7.3

For more information about virtualenv, checkout `its documentation <http://www.virtualenv.org/en/latest/>`_.

Commands
--------

See the available commands::

  pythonz help

To get help on each individual command run::

  pythonz help <command>

DTrace support
--------------

CPython versions 2.7.6 and 3.3.4 can be built with DTrace suport. Patches adding support
for DTrace have been taken from `this page <http://www.jcea.es/artic/solitaire.htm/python_dtrace.htm>`_
by Jesús Cea.

Building Python with DTrace support::

  pythonz install --configure="--with-dtrace" 2.7.6

