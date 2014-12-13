
import os
import shutil


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

PYTHONZ_ROOT = '/tmp/pythonz.test'
TESTPY_VERSION = (
    ('cpython', ['2.6.8', '2.7.3', '3.3.0']),
    ('stackless', ['2.7.2', '3.2.2']),
    ('pypy', ['1.9']),
    ('jython', ['2.5.3']),
)


def _cleanall():
    if os.path.isdir(PYTHONZ_ROOT):
        shutil.rmtree(PYTHONZ_ROOT)


def _install_pythonz():
    from pythonz.installer import install_pythonz
    install_pythonz()


def setup():
    os.environ['PYTHONZ_ROOT'] = PYTHONZ_ROOT
    _cleanall()
    _install_pythonz()


def teardown():
    _cleanall()


class Options(object):
    """A mock options object."""

    def __init__(self, opts):
        vars(self).update(opts)


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

def test_01_update():
    from pythonz.commands.update import UpdateCommand
    c = UpdateCommand()
    c.run_command(None, None)


def test_02_help():
    from pythonz.commands.help import HelpCommand
    c = HelpCommand()
    c.run_command(None, None)


def test_03_install():
    from pythonz.commands.install import InstallCommand
    for t, versions in TESTPY_VERSION:
        o = Options({'type': t, 'force':True, 'run_tests':False, 'url': None,
                     'file': None, 'verbose':False, 'configure': "",
                     'framework':False, 'universal':False, 'shared':False})
        c = InstallCommand()
        c.run_command(o, [versions.pop()]) # pythonz install 2.5.5
        if versions:
            c.run_command(o, versions) # pythonz install 2.6.6 2.7.3 3.2


def test_04_list():
    from pythonz.commands.list import ListCommand
    c = ListCommand()
    c.run_command(Options({'all_versions': False}), None)


def test_05_uninstall():
    from pythonz.commands.uninstall import UninstallCommand
    for py_type, py_versions in TESTPY_VERSION:
        c = UninstallCommand()
        for py_version in py_versions:
            c.run_command(Options({'type': py_type}), [py_version])


def test_06_cleanup():
    from pythonz.commands.cleanup import CleanupCommand
    c = CleanupCommand()
    c.run_command(Options({'clean_all': False}), None)
    c.run_command(Options({'clean_all': True}), None)

