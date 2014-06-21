
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.installer.pythoninstaller import CPythonInstaller, StacklessInstaller, PyPyInstaller, PyPy3Installer, JythonInstaller
from pythonz.log import logger


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

    def run_command(self, options, args):
        if options.all_versions:
            self.all()
        else:
            self.installed(path=options.path)

    def installed(self, path):
        logger.log("# Installed Python versions")
        for d in sorted(os.listdir(PATH_PYTHONS)):
            if path:
                logger.log('  %-16s %s/%s' % (d, PATH_PYTHONS, d))
            else:
                logger.log('  %s' % d)

    def all(self):
        logger.log('# Available Python versions')
        for type, installer in zip(['cpython', 'stackless', 'pypy', 'pypy3', 'jython'], [CPythonInstaller, StacklessInstaller, PyPyInstaller, PyPy3Installer, JythonInstaller]):
            logger.log('  # %s:' % type)
            for version in installer.supported_versions:
                logger.log('     %s' % version)

ListCommand()

