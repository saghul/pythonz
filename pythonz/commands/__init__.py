
import os
import re
import sys

from optparse import OptionParser


command_map = {}

class Command(object):
    name = None
    usage = None
    summary = ''

    def __init__(self):
        self.parser = OptionParser(usage=self.usage, prog='pythonz %s' % self.name)
        command_map[self.name] = self

    def run(self, args):
        options, args = self.parser.parse_args(args)
        self.run_command(options, args)

def load_commands():
    modules = ['pythonz.commands.%s' % os.path.splitext(file)[0] for file in os.listdir(os.path.dirname(__file__)) if os.path.splitext(file)[1] == '.py' and file != os.path.basename(__file__)]
    list(map(__import__, modules))

