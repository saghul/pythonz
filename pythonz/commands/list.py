
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.installer.pythoninstaller import CPythonInstaller, StacklessInstaller, PyPyInstaller, PyPy3Installer, JythonInstaller
from pythonz.log import logger


PY_TYPES = ['cpython', 'stackless', 'pypy', 'pypy3', 'jython']


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
        groups = zip(PY_TYPES,
                     [CPythonInstaller, StacklessInstaller, PyPyInstaller,
                      PyPy3Installer, JythonInstaller])

        if py_type:
            groups = filter(lambda (impl, _): impl in py_type, groups)

        for type_, installer in groups:
            logger.log('  # %s:' % type_)
            for version in sorted(installer.supported_versions):
                logger.log('     %s' % version)

ListCommand()
