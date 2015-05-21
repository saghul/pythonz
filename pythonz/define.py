
import os

# pythonz installer root path
INSTALLER_ROOT = os.path.dirname(os.path.abspath(__file__))

HOME = os.environ.get('HOME')
SYSTEMWIDE_PATH = '/usr/local/pythonz'

# Root
# pythonz root path
PYTHONZ_ROOT = os.environ.get('PYTHONZ_ROOT')
if   ( PYTHONZ_ROOT
       and os.path.isdir(PYTHONZ_ROOT) ):
    ROOT = PYTHONZ_ROOT
elif ( HOME
       and os.path.isdir(os.path.join(HOME, '.pythonz')) ):
    ROOT = os.path.join(HOME, '.pythonz')
elif os.path.isdir(SYSTEMWIDE_PATH):
    ROOT = SYSTEMWIDE_PATH
else:
    print "No installation of pythonz found."
    sys.exit(1)

# directories
PATH_PYTHONS = os.path.join(ROOT, 'pythons')
PATH_BUILD = os.path.join(ROOT, 'build')
PATH_DISTS = os.path.join(ROOT, 'dists')
PATH_ETC = os.path.join(ROOT, 'etc')
PATH_BASH_COMPLETION = os.path.join(PATH_ETC, 'bash_completion.d')
PATH_BIN = os.path.join(ROOT, 'bin')
PATH_LOG = os.path.join(ROOT, 'log')
PATH_SCRIPTS = os.path.join(ROOT, 'scripts')
PATH_SCRIPTS_PYTHONZ = os.path.join(PATH_SCRIPTS, 'pythonz')
PATH_SCRIPTS_PYTHONZ_COMMANDS = os.path.join(PATH_SCRIPTS_PYTHONZ, 'commands')
PATH_SCRIPTS_PYTHONZ_INSTALLER = os.path.join(PATH_SCRIPTS_PYTHONZ, 'installer')
PATH_PATCHES = os.path.join(ROOT, 'patches')
PATH_PATCHES_ALL = os.path.join(PATH_PATCHES, 'all')
PATH_PATCHES_OSX = os.path.join(PATH_PATCHES, 'osx')

# files
PATH_BIN_PYTHONZ = os.path.join(PATH_BIN, 'pythonz')

# Home
# pythonz home path
PYTHONZ_HOME = os.environ.get('PYTHONZ_HOME')
if   ( PYTHONZ_HOME
       and os.path.isdir(PYTHONZ_HOME) ):
    PATH_HOME = PYTHONZ_HOME
elif HOME:
    PATH_HOME = os.path.join(HOME, '.pythonz')
elif os.path.isdir(SYSTEMWIDE_PATH):
    PATH_HOME = SYSTEMWIDE_PATH
else:
    print "No home directory for pythonz found."
    sys.exit(1)

# directories
PATH_HOME_ETC = os.path.join(PATH_HOME, 'etc')

# pythonz download
PYTHONZ_UPDATE_URL = 'https://github.com/saghul/pythonz/archive/master.tar.gz'

