
from pythonz.installer.pythonzinstaller import pythonzInstaller
from pythonz.log import logger
from pythonz.define import INSTALLER_ROOT, ROOT, PATH_ETC

def install_pythonz():
    pythonzInstaller.install(INSTALLER_ROOT)
    # for bash
    shrc = yourshrc = "bashrc"
    logger.log("""
Well-done! Congratulations!

The pythonz is installed as:

  %(ROOT)s

Please add the following line to the end of your ~/.%(yourshrc)s

  source %(PATH_ETC)s/%(shrc)s

After that, exit this shell, start a new one, and install some fresh
pythons:

  pythonz install 2.7.2
  pythonz install 3.2

For further instructions, run:

  pythonz help

The default help messages will popup and tell you what to do!

Enjoy pythonz at %(ROOT)s!!
""" % {'ROOT':ROOT, 'yourshrc':yourshrc, 'shrc':shrc, 'PATH_ETC':PATH_ETC})

def upgrade_pythonz():
    pythonzInstaller.install(INSTALLER_ROOT)

def systemwide_pythonz():
    pythonzInstaller.install(INSTALLER_ROOT)
    pythonzInstaller.systemwide_install()
    logger.log("""
Well-done! Congratulations!

The pythonz is installed as:

  %(ROOT)s

After that, exit this shell, start a new one, and install some fresh
pythons:

  pythonz install 2.7.2
  pythonz install 3.2

For further instructions, run:

  pythonz help

The default help messages will popup and tell you what to do!

Enjoy pythonz at %(ROOT)s!!
""" % {'ROOT':ROOT})

