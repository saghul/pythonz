
from pythonz.basecommand import Command
from pythonz.util import off

class OffCommand(Command):
    name = "off"
    usage = "%prog"
    summary = "Disable pythonz"
    
    def run_command(self, options, args):
        off()

OffCommand()

