
import os
import sys

from pythonz.commands import command_map, load_commands
from pythonz.baseparser import parser
from pythonz.define import PATH_HOME_ETC
from pythonz.util import makedirs


def init_home():
    if not os.path.isdir(PATH_HOME_ETC):
        makedirs(PATH_HOME_ETC)

def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help'] # as default
    init_home()
    load_commands()
    command = args[0].lower()
    if command not in command_map:
        parser.error("Unknown command: `%s`" % command)
        return
    command = command_map[command]
    command.run(args[1:])

