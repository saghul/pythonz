
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
    current_dir = os.listdir(os.path.dirname(__file__))
    current_base = os.path.basename(__file__)
    for filename in current_dir:
        name, ext = os.path.splitext(filename)
        if ext == '.py' and name != current_base:
            __import__('pythonz.commands.%s' % name)
