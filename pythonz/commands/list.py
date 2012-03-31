
import os
from pythonz.basecommand import Command
from pythonz.define import PYTHON_VERSION_URL, PATH_PYTHONS
from pythonz.util import get_using_python_pkgname
from pythonz.log import logger

class ListCommand(Command):
    name = "list"
    usage = "%prog"
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
    
    def run_command(self, options, args):
        if options.all_versions:
            self.all()
        else:
            self.installed()
    
    def installed(self):
        logger.log("# Installed Python versions")
        cur = get_using_python_pkgname()
        for d in sorted(os.listdir(PATH_PYTHONS)):
            if cur and cur == d:
                logger.log('  %s (*)' % d)
            else:
                logger.log('  %s' % d)
    
    def all(self):
        logger.log('# Available Python versions')
        for version in (version for version in sorted(PYTHON_VERSION_URL.keys())):
            logger.log("Python-%s" % version)
    
ListCommand()

