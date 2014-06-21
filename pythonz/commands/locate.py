
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.util import Package, is_installed
from pythonz.log import logger


class LocateCommand(Command):
    name = "locate"
    usage = "%prog [options] VERSION"
    summary = "Locate the given version of python"

    def __init__(self):
        super(LocateCommand, self).__init__()
        self.parser.add_option(
            "-t", "--type",
            dest="type",
            default="cpython",
            help="Type of Python version: cpython, stackless, pypy, pypy3 or jython."
        )

    def run_command(self, options, args):
        if not args or len(args) > 1:
            self.parser.print_help()
            return

        pkg = Package(args[0], options.type)
        pkgname = pkg.name
        if not is_installed(pkg):
            logger.error("`%s` is not installed." % pkgname)
            return
        logger.log(os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python'))

LocateCommand()

