
import os

from optparse import OptionParser


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        '-U', '--upgrade',
        dest="upgrade",
        action="store_true",
        default=False,
        help="Upgrade."
    )
    parser.add_option(
        '--systemwide',
        dest="systemwide",
        action="store_true",
        default=False,
        help="systemwide install."
    )
    opt, arg = parser.parse_args()
    if opt.systemwide:
        os.environ['PYTHONZ_ROOT'] = '/usr/local/pythonz'
        from pythonz.installer import systemwide_pythonz
        systemwide_pythonz()
    elif opt.upgrade:
        from pythonz.installer import upgrade_pythonz
        upgrade_pythonz()
    else:
        from pythonz.installer import install_pythonz
        install_pythonz()

