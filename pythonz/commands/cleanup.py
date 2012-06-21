
import os

from pythonz.commands import Command
from pythonz.define import PATH_BUILD, PATH_DISTS
from pythonz.util import rm_r


class CleanupCommand(Command):
    name = "cleanup"
    usage = "%prog"
    summary = "Remove stale source folders and archives"

    def __init__(self):
        super(CleanupCommand, self).__init__()
        self.parser.add_option(
            '-a', '--all',
            dest='clean_all',
            action='store_true',
            default=False,
            help='Clean all, including the build directory. Note that debug symbols will be gone too!'
        )

    def run_command(self, options, args):
        if options.clean_all:
            self._cleanup(PATH_BUILD)
        self._cleanup(PATH_DISTS)

    def _cleanup(self, root):
        for dir in os.listdir(root):
            rm_r(os.path.join(root, dir))

CleanupCommand()

