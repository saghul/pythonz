
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.installer.pythoninstaller import CPythonInstaller, StacklessInstaller, PyPyInstaller, PyPy3Installer, JythonInstaller
from pythonz.log import logger


PY_INSTALLERS = {'cpython': CPythonInstaller,
                 'stackless': StacklessInstaller,
                 'pypy': PyPyInstaller,
                 'pypy3': PyPy3Installer,
                 'jython': JythonInstaller}

PY_TYPES = sorted(PY_INSTALLERS.keys())



class ListCommand(Command):
    name = "list"
    usage = "%prog [options]"
    summary = "List the installed python versions"

    def __init__(self):
        super(ListCommand, self).__init__()
        self.parser.add_option(
            '-a', '--all-versions',
            dest='all_versions',
            action='store_true',
            default=False,
            help='Show the all available python versions.'
        )
        self.parser.add_option(
            '-p', '--path',
            dest='path',
            action='store_true',
            default=False,
            help='Show the path for all Python installations.'
        )
        self.parser.add_option(
            '-t', '--type',
            dest='py_type',
            choices=PY_TYPES,
            default=[],
            help=('Use with -a to list only certain Python types. '
                  'Available choices: {0}'.format(PY_TYPES))
        )

    def run_command(self, options, args):
        if options.all_versions:
            self.all(py_type=options.py_type)
        else:
            self.installed(path=options.path)

    def installed(self, path):
        logger.log("# Installed Python versions")
        for d in sorted(os.listdir(PATH_PYTHONS)):
            if path:
                logger.log('  %-16s %s/%s' % (d, PATH_PYTHONS, d))
            else:
                logger.log('  %s' % d)

    def all(self, py_type):
        logger.log('# Available Python versions')
        py_types = [py_type] if py_type else PY_TYPES

        for type_ in py_types:
            logger.log('  # %s:' % type_)
            for version in sorted(PY_INSTALLERS[type_].supported_versions):
                logger.log('     %s' % version)

ListCommand()
