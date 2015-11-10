
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.installer.pythoninstaller import CPythonInstaller, StacklessInstaller, PyPyInstaller, PyPy3Installer, JythonInstaller
from pythonz.log import logger


class ListCommand(Command):
    name = "list"
    usage = "%prog [options] [filter]"
    summary = "List the installed python versions"

    def __init__(self):
        super(ListCommand, self).__init__()
        self.parser.add_option(
            '-a', '--all-versions',
            dest='all_versions',
            action='store_true',
            default=False,
            help=('Show the all available python versions. Optionally, show '
                  'chosen implementations. e.g.: pythonz list -a pypy3')
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
            self.all(args)
        else:
            self.installed(path=options.path)

    def installed(self, path):
        logger.log("# Installed Python versions")
        for d in sorted(os.listdir(PATH_PYTHONS)):
            if path:
                logger.log('  %-16s %s/%s' % (d, PATH_PYTHONS, d))
            else:
                logger.log('  %s' % d)

    def all(self, implementations):
        logger.log('# Available Python versions')
        groups = zip(['cpython', 'stackless', 'pypy', 'pypy3', 'jython'],
                     [CPythonInstaller, StacklessInstaller, PyPyInstaller,
                      PyPy3Installer, JythonInstaller])

        if implementations:
            groups = filter(lambda (impl, _): impl in implementations, groups)

        for type_, installer in groups:
            logger.log('  # %s:' % type_)
            for version in installer.supported_versions:
                logger.log('     %s' % version)

ListCommand()
