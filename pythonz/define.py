
import os

# pythonz installer root path
INSTALLER_ROOT = os.path.dirname(os.path.abspath(__file__))

# Root
# pythonz root path
SYSTEMWIDE_PATH = '/usr/local/pythonz'
ROOT = os.environ.get('PYTHONZ_ROOT') or os.path.join(os.environ['HOME'], '.pythonz') if not os.path.abspath(os.path.dirname(__file__)).startswith(SYSTEMWIDE_PATH) else SYSTEMWIDE_PATH

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

PATH_PATCHES = os.path.join(INSTALLER_ROOT, 'patches')
PATH_PATCHES_ALL = os.path.join(PATH_PATCHES, 'all')
PATH_PATCHES_OSX = os.path.join(PATH_PATCHES, 'osx')

# files
PATH_BIN_PYTHONZ = os.path.join(PATH_BIN, 'pythonz')

# Home
# pythonz home path
PATH_HOME = os.environ.get('PYTHONZ_HOME') or os.path.join(os.environ['HOME'], '.pythonz')

# directories
PATH_HOME_ETC = os.path.join(PATH_HOME, 'etc')

# pythonz download
PYTHONZ_UPDATE_URL = 'https://github.com/saghul/pythonz/archive/master.tar.gz'
