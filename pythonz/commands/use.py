
import os
import sys

from pythonz.basecommand import Command
from pythonz.define import PATH_PYTHONS, PATH_HOME_ETC_TEMP
from pythonz.util import Package
from pythonz.log import logger


class UseCommand(Command):
    name = "use"
    usage = "%prog [options] VERSION"
    summary = "Use the specified python in current shell"

    def __init__(self):
        super(UseCommand, self).__init__()
        self.parser.add_option(
            "-t", "--type",
            dest="type",
            default="cpython",
            help="Type of Python version: cpython, stackless or pypy."
        )

    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        pkg = Package(args[0], options.type)
        pkgname = pkg.name
        pkgdir = os.path.join(PATH_PYTHONS, pkgname)
        if not os.path.isdir(pkgdir):
            logger.error("`%s` is not installed." % pkgname)
            sys.exit(1)
        pkgbin = os.path.join(pkgdir,'bin')

        self._set_temp(pkgbin)

        logger.info("Using `%s`" % pkgname)

    def _set_temp(self, path):
        with open(PATH_HOME_ETC_TEMP, 'w') as f:
            f.write('PATH_PYTHONZ_TEMP="%s"\n' % (path))

UseCommand()

