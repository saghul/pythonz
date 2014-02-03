
from pythonz.commands import Command
from pythonz.log import logger
from pythonz.version import __version__


class VersionCommand(Command):
    name = "version"
    usage = "%prog"
    summary = "Show version"

    def run_command(self, options, args):
        logger.log(__version__)

VersionCommand()

