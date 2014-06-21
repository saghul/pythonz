
import os

from pythonz.commands import Command
from pythonz.define import PATH_PYTHONS
from pythonz.util import rm_r, Package, is_installed
from pythonz.log import logger


class UninstallCommand(Command):
    name = "uninstall"
    usage = "%prog [options] VERSION"
    summary = "Uninstall the given version of python"

    def __init__(self):
        super(UninstallCommand, self).__init__()
        self.parser.add_option(
            "-t", "--type",
            dest="type",
            default="cpython",
            help="Type of Python version: cpython, stackless, pypy, pypy3 or jython."
        )

    def run_command(self, options, args):
        if args:
            # Uninstall pythons
            for arg in args:
                pkg = Package(arg, options.type)
                pkgname = pkg.name
                if not is_installed(pkg):
                    logger.error("`%s` is not installed." % pkgname)
                    continue
                rm_r(os.path.join(PATH_PYTHONS, pkgname))
        else:
            self.parser.print_help()

UninstallCommand()

