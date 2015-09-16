
import os
import sys
import glob
import shutil
import stat
import time

from pythonz.util import makedirs, rm_r
from pythonz.define import PATH_BUILD, PATH_BIN, PATH_DISTS, PATH_PYTHONS,\
    PATH_ETC, PATH_SCRIPTS, PATH_SCRIPTS_PYTHONZ,\
    PATH_SCRIPTS_PYTHONZ_COMMANDS, PATH_BIN_PYTHONZ, PATH_LOG,\
    PATH_SCRIPTS_PYTHONZ_INSTALLER, PATH_HOME_ETC, ROOT,\
    PATH_BASH_COMPLETION


class PythonzInstaller(object):
    """pythonz installer:
    """

    @staticmethod
    def install(installer_root):
        # create directories
        makedirs(PATH_PYTHONS)
        makedirs(PATH_BUILD)
        makedirs(PATH_DISTS)
        makedirs(PATH_ETC)
        makedirs(PATH_BASH_COMPLETION)
        makedirs(PATH_BIN)
        makedirs(PATH_LOG)
        makedirs(PATH_HOME_ETC)

        # create script directories
        rm_r(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS_PYTHONZ)
        makedirs(PATH_SCRIPTS_PYTHONZ_COMMANDS)
        makedirs(PATH_SCRIPTS_PYTHONZ_INSTALLER)

        # copy all .py files
        for path in glob.glob(os.path.join(installer_root,"*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONZ)
        for path in glob.glob(os.path.join(installer_root,"commands","*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONZ_COMMANDS)
        for path in glob.glob(os.path.join(installer_root,"installer","*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONZ_INSTALLER)

        # create a main file
        with open("%s/pythonz_main.py" % PATH_SCRIPTS, "w") as f:
            f.write("""import pythonz
if __name__ == "__main__":
    pythonz.main()
""")

        # create entry point file
        with open(PATH_BIN_PYTHONZ, "w") as f:
            f.write("""#!/usr/bin/env bash
python %s/pythonz_main.py "$@"
""" % PATH_SCRIPTS)

        # mode 0755
        os.chmod(PATH_BIN_PYTHONZ, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

        # create a bashrc for pythonz
        shutil.copy(os.path.join(installer_root,'etc','bashrc'), os.path.join(PATH_ETC,'bashrc'))

        # create a fish file for pythonz
        shutil.copy(os.path.join(installer_root, 'etc', 'pythonz.fish'), os.path.join(PATH_ETC, 'pythonz.fish'))

        #copy all *.sh files to bash_completion.d directory
        for path in glob.glob(os.path.join(installer_root,"etc","bash_completion.d","*.sh")):
            shutil.copy( path, PATH_BASH_COMPLETION )

    @staticmethod
    def systemwide_install():
        profile = """\
#begin-pythonz
if [ -n "${BASH_VERSION:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    export PYTHONZ_ROOT=%(root)s
    source "${PYTHONZ_ROOT}/etc/bashrc"
fi
#end-pythonz
""" % {'root': ROOT}

        if os.path.isdir('/etc/profile.d'):
            with open('/etc/profile.d/pythonz.sh', 'w') as f:
                f.write(profile)
        elif os.path.isfile('/etc/profile'):
            # create backup
            shutil.copy('/etc/profile', '/tmp/profile.pythonz.%s' % int(time.time()))

            output = []
            is_copy = True
            with open('/etc/profile', 'r') as f:
                for line in f:
                    if line.startswith('#begin-pythonz'):
                        is_copy = False
                        continue
                    elif line.startswith('#end-pythonz'):
                        is_copy = True
                        continue
                    if is_copy:
                        output.append(line)
            output.append(profile)

            with open('/etc/profile', 'w') as f:
                f.write(''.join(output))
