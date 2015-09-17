
import sys

from pythonz.commands import Command
from pythonz.installer.pythoninstaller import PythonInstaller, AlreadyInstalledError
from pythonz.log import logger


class InstallCommand(Command):
    name = "install"
    usage = "%prog [OPTIONS] VERSION"
    summary = "Build and install the given version of python"

    def __init__(self):
        super(InstallCommand, self).__init__()
        self.parser.add_option(
            "-t", "--type",
            dest="type",
            default="cpython",
            help="Type of Python version: cpython, stackless, pypy, pypy3 or jython."
        )
        self.parser.add_option(
            "-f", "--force",
            dest="force",
            action="store_true",
            default=False,
            help="Force installation of python even if tests fail."
        )
        self.parser.add_option(
            "--run-tests",
            dest="run_tests",
            action="store_true",
            default=False,
            help="Run `make test` after compiling."
        )
        self.parser.add_option(
            "--url",
            dest="url",
            default=None,
            help="URL used to download the specified python version."
        )
        self.parser.add_option(
            "--file",
            dest="file",
            default=None,
            help="File pinting to the python version to be installed."
        )
        self.parser.add_option(
            "-v", "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Display log information on the console."
        )
        self.parser.add_option(
            "-C", "--configure",
            dest="configure",
            default="",
            metavar="CONFIGURE_OPTIONS",
            help="Options passed directly to configure."
        )
        self.parser.add_option(
            "--framework",
            dest="framework",
            action="store_true",
            default=False,
            help="Build Framework. (OSX only)"
        )
        self.parser.add_option(
            "--universal",
            dest="universal",
            action="store_true",
            default=False,
            help="Build for both 32 & 64 bit Intel. (OSX only)"
        )
        self.parser.add_option(
            "--shared",
            dest="shared",
            action="store_true",
            default=False,
            help="Build shared libraries."
        )
        self.parser.add_option(
            "--reinstall",
            dest="reinstall",
            action="store_true",
            default=False,
            help="Reinstall Python version, if already installed."
        )

    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        for arg in args:
            try:
                p = PythonInstaller.get_installer(arg, options)
                p.install()
            except AlreadyInstalledError as e:
                logger.info(e)
            except Exception:
                import traceback
                traceback.print_exc()
                continue

InstallCommand()
