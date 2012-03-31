
import os

from pythonz.basecommand import Command
from pythonz.define import PATH_PYTHONS
from pythonz.util import off, rm_r, Package, get_using_python_pkgname, is_installed
from pythonz.log import logger


class UninstallCommand(Command):
    name = "uninstall"
    usage = "%prog VERSION"
    summary = "Uninstall the given version of python"

    def __init__(self):
        super(UninstallCommand, self).__init__()
        self.parser.add_option(
            "-t", "--type",
            dest="type",
            default="cpython",
            help="Force installation of python even if tests fail."
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
                if get_using_python_pkgname() == pkgname:
                    off()
                rm_r(os.path.join(PATH_PYTHONS, pkgname))
        else:
            self.parser.print_help()

UninstallCommand()

