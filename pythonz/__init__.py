
import os
import sys

from optparse import OptionParser

from pythonz.commands import command_map, load_commands
from pythonz.define import PATH_HOME_ETC, PATH_PYTHONS
from pythonz.util import makedirs


parser = OptionParser(usage="%prog COMMAND [OPTIONS]",
                      prog="pythonz",
                      add_help_option=False)
parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')
parser.disable_interspersed_args()


def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help'] # as default

    makedirs(PATH_PYTHONS)
    makedirs(PATH_HOME_ETC)

    load_commands()
    command = args[0].lower()

    try:
        command = command_map[command]
    except KeyError:
        parser.error("Unknown command: `%s`" % command)
        return
    try:
        command.run(args[1:])
    except KeyboardInterrupt:
        pass

