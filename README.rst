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
----------------------------------------

If the install script is run as root, pythonz will automatically install into ``/usr/local/pythonz``.

pythonz will be automatically configured for every user on the system if you install it as root.

After installing it, where you would normally use `sudo`, non-root users will need to use `sudo-pythonz`::

  sudo-pythonz install 2.7.3

Before installing Pythons via Pythonz
-------------------------------------

You might want to install some optional dependencies, for functionality that
is often expected to be included in a Python build (it can be a bummer to discover these missing and
have to rebuild your python setup). These include the following, ordered by (very roughly guessed)
probability that you will need them::

Debian family (Ubuntu...)
^^^^^^^^^^^^^^^^^^^^^^^^^

::

  sudo apt-get install build-essential zlib1g-dev libbz2-dev libssl-dev libreadline-dev libncurses5-dev libsqlite3-dev libgdbm-dev libdb-dev libexpat-dev libpcap-dev liblzma-dev libpcre3-dev

If you need tkinter support, add **tk-dev**.

RPM family (CentOS, RHEL...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  yum groupinstall "Development tools"
  yum install zlib-devel bzip2-devel openssl-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel expat-devel libpcap-devel xz-devel pcre-devel

If you need tkinter support, add **tk-devel**.

OSX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  xcode-select --install

Usage
-----

::

  pythonz command [options] version

See the available commands
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz help

To get help on each individual command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz help <command>


Install some pythons
^^^^^^^^^^^^^^^^^^^^

::

  pythonz install 2.7.3
  pythonz install -t stackless 2.7.2
  pythonz install -t jython 2.5.2
  pythonz install -t pypy --url https://bitbucket.org/pypy/pypy/downloads/pypy-1.8-osx64.tar.bz2 1.8
  pythonz install --verbose 2.7.2
  pythonz install --configure="CC=gcc_4.1" 2.7.2
  pythonz install --url http://www.python.org/ftp/python/2.7/Python-2.7.2.tgz 2.7.2
  pythonz install --file /path/to/Python-2.7.2.tgz 2.7.2
  pythonz install 2.7.3 3.2.3
  pythonz install -t pypy3 2.3.1

List the installed pythons
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz list

List all the available python versions for installing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz list -a

Uninstall the specified python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz uninstall 2.7.3
  pythonz uninstall -t stackless 3.2.2

Remove stale source folders and archives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz cleanup

Upgrade pythonz to the latest version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz update

Check the installed pythonz version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz version

Print the path to the interpreter of a given version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  pythonz locate 2.7.7

Recommended way to use a pythonz-installed version of Python
------------------------------------------------------------

For Python <= 3.2
^^^^^^^^^^^^^^^^^

Use `virtualenv`, e.g.::

  mkvirtualenv -p $(pythonz locate 2.7.3) python2.7.3

For more information about virtualenv, checkout `its documentation <http://www.virtualenv.org/en/latest/>`_.

For Python >= 3.3
^^^^^^^^^^^^^^^^^

Use `pyvenv` directly from Python, e.g.::

  /usr/local/pythonz/pythons/CPython-3.4.1/bin/pyvenv pyvenv

For more information about pyvenv, checkout `its documentation <https://docs.python.org/3/library/venv.html>`_.

DTrace support
--------------

CPython versions 2.7.6 and 3.3.4 can be built with DTrace suport. Patches adding support
for DTrace have been taken from `this page <http://www.jcea.es/artic/solitaire.htm/python_dtrace.htm>`_
by Jesús Cea.

Building Python with DTrace support::

  pythonz install --configure="--with-dtrace" 2.7.6

