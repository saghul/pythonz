
import ctypes
import os
import sys
import shutil
import mimetypes
import multiprocessing
import re
import subprocess

from pythonz.util import symlink, Package, is_url, Link,\
    unlink, is_html, Subprocess, rm_r, is_python26, is_python27,\
    extract_downloadfile, is_archive_file, path_to_fileurl, is_file,\
    fileurl_to_path, is_python30, is_python31, is_python32,\
    get_macosx_deployment_target, Version, is_python25, is_python24
from pythonz.define import PATH_BUILD, PATH_DISTS, PATH_PYTHONS, PATH_LOG, \
    PATH_PATCHES_ALL, PATH_PATCHES_OSX
from pythonz.downloader import Downloader
from pythonz.log import logger
from pythonz.exceptions import DownloadError, UnknownVersionException


class PythonInstaller(object):
    @staticmethod
    def get_installer(version, options):
        type = options.type.lower()
        if type == 'cpython':
            return CPythonInstaller(version, options)
        elif type == 'stackless':
            return StacklessInstaller(version, options)
        elif type == 'pypy':
            return PyPyInstaller(version, options)
        elif type == 'jython':
            return JythonInstaller(version, options)
        raise RuntimeError('invalid type specified: %s' % type)


class Installer(object):
    supported_versions = []

    def __init__(self, version, options):
        if options.file is not None:
            if not (is_archive_file(options.file) and os.path.isfile(options.file)):
                logger.error('invalid file specified: %s' % options.file)
                raise RuntimeError
            self.download_url = path_to_fileurl(options.file)
        elif options.url is not None:
            if not is_url(options.url):
                logger.error('invalid URL specified: %s' % options.url)
                raise RuntimeError
            self.download_url = options.url
        else:
            if version not in self.supported_versions:
                logger.error("Unsupported Python version: `%s`, you may install it anyway by supplying the download or file URL" % version)
                raise UnknownVersionException
            self.download_url = self.get_version_url(version)
        self.pkg = Package(version, options.type)
        self.install_dir = os.path.join(PATH_PYTHONS, self.pkg.name)
        self.build_dir = os.path.join(PATH_BUILD, self.pkg.name)
        filename = Link(self.download_url).filename
        self.download_file = os.path.join(PATH_DISTS, filename)

        self.options = options
        self.logfile = os.path.join(PATH_LOG, 'build.log')
        self.patches = []
        self.configure_options = []

    @classmethod
    def get_version_url(cls, version):
        # Version is known to be in supported_versions
        raise NotImplementedError

    def download(self):
        if os.path.isfile(self.download_file):
            logger.info("Use the previously fetched %s" % (self.download_file))
        else:
            base_url = Link(self.download_url).base_url
            logger.info("Downloading %s as %s" % (base_url, self.download_file))
            try:
                Downloader.fetch(self.download_url, self.download_file)
            except DownloadError:
                unlink(self.download_file)
                logger.error("Failed to download.\n%s" % (sys.exc_info()[1]))
                sys.exit(1)

    def install(self):
        raise NotImplementedError


class CPythonInstaller(Installer):
    supported_versions = ['2.4', '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5', '2.4.6',
                          '2.5', '2.5.1', '2.5.2', '2.5.3', '2.5.4', '2.5.5', '2.5.6',
                          '2.6', '2.6.1', '2.6.2', '2.6.3', '2.6.4', '2.6.5', '2.6.6', '2.6.7', '2.6.8',
                          '2.7', '2.7.1', '2.7.2', '2.7.3',
                          '3.0', '3.0.1',
                          '3.1', '3.1.1', '3.1.2', '3.1.3', '3.1.4', '3.1.5',
                          '3.2', '3.2.1', '3.2.2', '3.2.3',
                          '3.3.0']

    def __init__(self, version, options):
        super(CPythonInstaller, self).__init__(version, options)

        if Version(self.pkg.version) >= '3.1':
            self.configure_options.append('--with-computed-gotos')

        if sys.platform == "darwin":
            # set configure options
            target = get_macosx_deployment_target()
            if target:
                self.configure_options.append('MACOSX_DEPLOYMENT_TARGET=%s' % target)

            # set build options
            if options.framework and options.static:
                logger.error("Can't specify both framework and static.")
                raise Exception
            if options.framework:
                self.configure_options.append('--enable-framework=%s' % os.path.join(self.install_dir, 'Frameworks'))
            elif not options.static:
                self.configure_options.append('--enable-shared')
            if options.universal:
                self.configure_options.append('--enable-universalsdk=/')
                self.configure_options.append('--with-universal-archs=intel')

    @classmethod
    def get_version_url(cls, version):
        # Version is known to be in supported_versions
        return 'http://www.python.org/ftp/python/%(version)s/Python-%(version)s.tgz' % {'version': version}

    def _apply_patches(self):
        try:
            s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
            for patch in self.patches:
                if type(patch) is dict:
                    for (ed, source) in patch.items():
                        s.shell('ed - %s < %s' % (source, ed))
                else:
                    s.shell("patch -p0 < %s" % patch)
        except:
            logger.error("Failed to patch `%s`.\n%s" % (self.build_dir, sys.exc_info()[1]))
            sys.exit(1)

    def _append_patch(self, patch_dir, patch_files):
        for patch in patch_files:
            if type(patch) is dict:
                tmp = patch
                patch = {}
                for key in tmp.keys():
                    patch[os.path.join(patch_dir, key)] = tmp[key]
                self.patches.append(patch)
            else:
                self.patches.append(os.path.join(patch_dir, patch))

    def install(self):
        # cleanup
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)

        # get content type.
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            self.content_type = mimetypes.guess_type(path)[0]
        else:
            headerinfo = Downloader.read_head_info(self.download_url)
            self.content_type = headerinfo['content-type']
        if is_html(self.content_type):
            # note: maybe got 404 or 503 http status code.
            logger.error("Invalid content-type: `%s`" % self.content_type)
            return

        if os.path.isdir(self.install_dir):
            logger.info("You have already installed `%s`" % self.pkg.name)
            return

        self.download_and_extract()
        logger.info("\nThis could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s\n" % self.logfile)
        logger.info("Installing %s into %s" % (self.pkg.name, self.install_dir))
        try:
            self.patch()
            self.configure()
            self.make()
            self.make_install()
        except Exception:
            import traceback
            traceback.print_exc()
            rm_r(self.install_dir)
            logger.error("Failed to install %s. Check %s to see why." % (self.pkg.name, self.logfile))
            sys.exit(1)
        self.symlink()
        logger.info("\nInstalled %(pkgname)s successfully." % {"pkgname": self.pkg.name})

    def download_and_extract(self):
        self.download()
        if not extract_downloadfile(self.content_type, self.download_file, self.build_dir):
            sys.exit(1)

    def _patch(self):
        version = Version(self.pkg.version)
        common_patch_dir = os.path.join(PATH_PATCHES_ALL, "common")
        if is_python26(version) or is_python25(version) or is_python24(version):
            self._append_patch(common_patch_dir, ['patch-setup.py.diff'])
        elif is_python27(version):
            if version < '2.7.2':
                self._append_patch(common_patch_dir, ['patch-setup.py.diff'])
        elif is_python30(version):
            patch_dir = os.path.join(PATH_PATCHES_ALL, "python30")
            self._append_patch(patch_dir, ['patch-setup.py.diff'])
        elif is_python31(version):
            if version < '3.1.4':
                self._append_patch(common_patch_dir, ['patch-setup.py.diff'])
        elif is_python32(version):
            if version == '3.2':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "python32")
                self._append_patch(patch_dir, ['patch-setup.py.diff'])

    def _patch_osx(self):
        version = Version(self.pkg.version)
        if is_python24(version):
            PATH_PATCHES_OSX_PYTHON24 = os.path.join(PATH_PATCHES_OSX, "python24")
            if version == '2.4':
                self._append_patch(PATH_PATCHES_OSX_PYTHON24, ['patch240-configure', 'patch240-setup.py.diff', 'patch240-Mac-OSX-Makefile.in', 'patch240-gestaltmodule.c.diff', 'patch240-sysconfig.py.diff'])
            elif version < '2.4.4':
                self._append_patch(PATH_PATCHES_OSX_PYTHON24, ['patch241-configure', 'patch240-setup.py.diff', 'patch240-Mac-OSX-Makefile.in', 'patch240-gestaltmodule.c.diff'])
            else:
                self._append_patch(PATH_PATCHES_OSX_PYTHON24, ['patch244-configure', 'patch244-setup.py.diff', 'patch244-Mac-OSX-Makefile.in', 'patch244-gestaltmodule.c.diff'])
            self._append_patch(PATH_PATCHES_OSX_PYTHON24, [
                                                  'patch-Makefile.pre.in',
                                                  'patch-Lib-cgi.py.diff',
                                                  'patch-Lib-site.py.diff',
                                                  'patch-Include-pyport.h',
                                                  'patch-configure-badcflags.diff',
                                                  'patch-macosmodule.diff',
                                                  'patch-mactoolboxglue.diff',
                                                  'patch-pymactoolbox.diff'])
        elif is_python25(version):
            PATH_PATCHES_OSX_PYTHON25 = os.path.join(PATH_PATCHES_OSX, "python25")
            if version == '2.5':
                self._append_patch(PATH_PATCHES_OSX_PYTHON25, ['patch250-setup.py.diff'])
            elif version == '2.5.1':
                self._append_patch(PATH_PATCHES_OSX_PYTHON25, ['patch251-setup.py.diff'])
            else:
                self._append_patch(PATH_PATCHES_OSX_PYTHON25, ['patch252-setup.py.diff'])
            self._append_patch(PATH_PATCHES_OSX_PYTHON25, [
                                                  'patch-Makefile.pre.in.diff',
                                                  'patch-Lib-cgi.py.diff',
                                                  'patch-Lib-distutils-dist.py.diff',
                                                  'patch-configure-badcflags.diff',
                                                  'patch-configure-arch_only.diff',
                                                  'patch-64bit.diff',
                                                  'patch-pyconfig.h.in.diff',
                                                  'patch-gestaltmodule.c.diff',
                                                  {'_localemodule.c.ed': 'Modules/_localemodule.c'},
                                                  {'locale.py.ed': 'Lib/locale.py'}])
        elif is_python26(version):
            PATH_PATCHES_OSX_PYTHON26 = os.path.join(PATH_PATCHES_OSX, "python26")
            self._append_patch(PATH_PATCHES_OSX_PYTHON26, [
                                                  'patch-Lib-cgi.py.diff',
                                                  'patch-Lib-distutils-dist.py.diff',
                                                  'patch-Mac-IDLE-Makefile.in.diff',
                                                  'patch-Mac-Makefile.in.diff',
                                                  'patch-Mac-PythonLauncher-Makefile.in.diff',
                                                  'patch-Mac-Tools-Doc-setup.py.diff',
                                                  'patch-setup.py-db46.diff',
                                                  'patch-Lib-ctypes-macholib-dyld.py.diff',
                                                  'patch-setup_no_tkinter.py.diff',
                                                  {'_localemodule.c.ed': 'Modules/_localemodule.c'},
                                                  {'locale.py.ed': 'Lib/locale.py'}])
        elif is_python27(version):
            PATH_PATCHES_OSX_PYTHON27 = os.path.join(PATH_PATCHES_OSX, "python27")
            self._append_patch(PATH_PATCHES_OSX_PYTHON27, [
                                                  'patch-Modules-posixmodule.diff'])

    def patch(self):
        if sys.platform == "darwin":
            self._patch_osx()
        else:
            self._patch()
        self._apply_patches()

    def configure(self):
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        cmd = "./configure --prefix=%s %s %s" % (self.install_dir, self.options.configure, ' '.join(self.configure_options))
        if self.options.verbose:
            logger.log(cmd)
        s.check_call(cmd)

    def make(self):
        try:
            jobs = multiprocessing.cpu_count()
        except NotImplementedError:
            make = 'make'
        else:
            make = 'make -j%s' % jobs
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        s.check_call(make)
        if self.options.run_tests:
            if self.options.force:
                # note: ignore tests failure error.
                s.call("make test")
            else:
                s.check_call("make test")

    def make_install(self):
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        s.check_call("make install")

    def symlink(self):
        install_dir = os.path.realpath(self.install_dir)
        if self.pkg.type == 'pypy':
            bin_dir = os.path.join(install_dir, 'bin')
            symlink(os.path.join(bin_dir, 'pypy'), os.path.join(bin_dir, 'python'))
            return
        if self.options.framework:
            # create symlink bin -> /path/to/Frameworks/Python.framework/Versions/?.?/bin
            bin_dir = os.path.join(install_dir, 'bin')
            if os.path.exists(bin_dir):
                rm_r(bin_dir)
            m = re.match(r'\d\.\d', self.pkg.version)
            if m:
                version = m.group(0)
            symlink(os.path.join(install_dir, 'Frameworks', 'Python.framework', 'Versions', version, 'bin'), os.path.join(bin_dir))
        path_python = os.path.join(install_dir, 'bin', 'python')
        if not os.path.isfile(path_python):
            src = None
            for d in os.listdir(os.path.join(install_dir, 'bin')):
                if re.match(r'python\d\.\d', d):
                    src = d
                    break
            if src:
                path_src = os.path.join(install_dir, 'bin', src)
                symlink(path_src, path_python)


class StacklessInstaller(CPythonInstaller):
    supported_versions = ['2.6.5',
                          '2.7.2',
                          '3.1.3',
                          '3.2.2']

    @classmethod
    def get_version_url(cls, version):
        # Version is known to be in supported_versions
        return 'http://www.stackless.com/binaries/stackless-%(version)s-export.tar.bz2' % {'version': version.replace('.', '')}


class PyPyInstaller(Installer):
    supported_versions = ['1.8',
                          '1.9']

    @classmethod
    def get_version_url(cls, version):
        # Version is known to be in supported_versions
        if sys.platform == 'darwin':
            return 'https://bitbucket.org/pypy/pypy/downloads/pypy-%(version)s-osx64.tar.bz2' % {'version': version}
        else:
            # Linux
            arch = {4: '', 8: 'x86_64'}[ctypes.sizeof(ctypes.c_size_t)]
            return 'https://bitbucket.org/pypy/pypy/downloads/pypy-%(version)s-linux%(arch)s.tar.bz2' % {'arch': arch, 'version': version}

    def install(self):
        # cleanup
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)

        # get content type.
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            self.content_type = mimetypes.guess_type(path)[0]
        else:
            headerinfo = Downloader.read_head_info(self.download_url)
            self.content_type = headerinfo['content-type']
        if is_html(self.content_type):
            # note: maybe got 404 or 503 http status code.
            logger.error("Invalid content-type: `%s`" % self.content_type)
            return

        if os.path.isdir(self.install_dir):
            logger.info("You have already installed `%s`" % self.pkg.name)
            return

        self.download_and_extract()
        logger.info("\nThis could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s\n" % self.logfile)
        logger.info("Installing %s into %s" % (self.pkg.name, self.install_dir))
        shutil.copytree(self.build_dir, self.install_dir)
        self.symlink()
        logger.info("\nInstalled %(pkgname)s successfully." % {"pkgname": self.pkg.name})

    def download_and_extract(self):
        self.download()
        if not extract_downloadfile(self.content_type, self.download_file, self.build_dir):
            sys.exit(1)

    def symlink(self):
        install_dir = os.path.realpath(self.install_dir)
        bin_dir = os.path.join(install_dir, 'bin')
        symlink(os.path.join(bin_dir, 'pypy'), os.path.join(bin_dir, 'python'))


class JythonInstaller(Installer):
    supported_versions = ['2.5.0', '2.5.1', '2.5.2', '2.5.3']

    @classmethod
    def get_version_url(cls, version):
        # Version is known to be in supported_versions
        if version in ('2.5.0', '2.5.1', '2.5.2'):
            return 'https://downloads.sourceforge.net/project/jython/jython/%(version)s/jython_installer-%(version)s.jar' % {'version': version}
        else:
            return 'http://search.maven.org/remotecontent?filepath=org/python/jython-installer/%(version)s/jython-installer-%(version)s.jar' % {'version': version}

    def install(self):
        # check if java is installed
        r = subprocess.call("command -v java > /dev/null", shell=True)
        if r != 0:
            logger.error("Jython requires Java to be installed, but the 'java' command was not found in the path.")
            return

        # cleanup
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)

        # get content type.
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            self.content_type = mimetypes.guess_type(path)[0]
        else:
            try:
                headerinfo = Downloader.read_head_info(self.download_url)
            except DownloadError:
                self.content_type = None
            else:
                self.content_type = headerinfo['content-type']
        if is_html(self.content_type):
            # note: maybe got 404 or 503 http status code.
            logger.error("Invalid content-type: `%s`" % self.content_type)
            return

        if os.path.isdir(self.install_dir):
            logger.info("You have already installed `%s`" % self.pkg.name)
            return

        self.download()
        logger.info("\nThis could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s\n" % self.logfile)
        logger.info("Installing %s into %s" % (self.pkg.name, self.install_dir))
        cmd = 'java -jar %s -s -d %s' % (self.download_file, self.install_dir)
        s = Subprocess(log=self.logfile, verbose=self.options.verbose)
        s.check_call(cmd)
        self.symlink()
        logger.info("\nInstalled %(pkgname)s successfully." % {"pkgname": self.pkg.name})

    def symlink(self):
        install_dir = os.path.realpath(self.install_dir)
        bin_dir = os.path.join(install_dir, 'bin')
        symlink(os.path.join(bin_dir, 'jython'), os.path.join(bin_dir, 'python'))


