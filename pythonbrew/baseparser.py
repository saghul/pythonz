from optparse import OptionParser

parser = OptionParser(usage="%prog COMMAND [OPTIONS]",
                      prog="pythonbrew",
                      add_help_option=False)
parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')
parser.disable_interspersed_args()
