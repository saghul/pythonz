
from optparse import OptionParser
from pythonz.installer import install_pythonz, upgrade_pythonz, systemwide_pythonz

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
        systemwide_pythonz()
    elif opt.upgrade:
        upgrade_pythonz()
    else:
        install_pythonz()

