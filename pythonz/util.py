
import os
import sys
import errno
import shutil
import re
import posixpath
import tarfile
import platform
import subprocess
import shlex
import select

PY3K = sys.version_info >= (3,)
if not PY3K:
    from urllib import quote as urlquote, unquote as urlunquote
    from urllib2 import urlparse
else:
    from urllib.parse import urlparse, quote as urlquote, unquote as urlunquote

from pythonz.define import PATH_PYTHONS
from pythonz.log import logger


def is_url(name):
    try:
        result = urlparse.urlparse(name)
    except Exception:
        return False
    else:
        return result.scheme in ('http', 'https', 'file', 'ftp')

def is_file(name):
    try:
        result = urlparse.urlparse(name)
    except Exception:
        return False
    else:
        return result.scheme == 'file'

def splitext(name):
    base, ext = os.path.splitext(name)
    if base.lower().endswith('.tar'):
        ext = base[-4:] + ext
        base = base[:-4]
    return base, ext

def is_archive_file(name):
    ext = splitext(name)[1].lower()
    return ext in ('.zip', '.tar.gz', '.tar.bz2', '.tgz', '.tar')

def is_html(content_type):
    return content_type and content_type.startswith('text/html')

def is_gzip(content_type, filename):
    return content_type == 'application/x-gzip' or tarfile.is_tarfile(filename) or splitext(filename)[1].lower() in ('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz')

def get_macosx_deployment_target():
    m = re.search('^([0-9]+\.[0-9]+)', platform.mac_ver()[0])
    if m:
        return m.group(1)
    return None

def _py_version_cmp(v, v1, v2):
    if is_str(v):
        v = Version(v)
    return v >= v1 and v < v2

def is_python24(version):
    return _py_version_cmp(version, '2.4', '2.5')

def is_python25(version):
    return _py_version_cmp(version, '2.5', '2.6')

def is_python26(version):
    return _py_version_cmp(version, '2.6', '2.7')

def is_python27(version):
    return _py_version_cmp(version, '2.7', '2.8')

def is_python30(version):
    return _py_version_cmp(version, '3.0', '3.1')

def is_python31(version):
    return _py_version_cmp(version, '3.1', '3.2')

def is_python32(version):
    return _py_version_cmp(version, '3.2', '3.3')

def is_python33(version):
    return _py_version_cmp(version, '3.3', '3.4')

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def symlink(src, dst):
    try:
        os.symlink(src, dst)
    except OSError:
        pass

def unlink(path):
    try:
        os.unlink(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def rm_r(path):
    """like rm -r command."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        unlink(path)

def split_leading_dir(path):
    path = str(path)
    path = path.lstrip('/').lstrip('\\')
    if '/' in path and (('\\' in path and path.find('/') < path.find('\\')) or '\\' not in path):
        return path.split('/', 1)
    elif '\\' in path:
        return path.split('\\', 1)
    else:
        return path, ''

def has_leading_dir(paths):
    """Returns true if all the paths have the same leading path name
    (i.e., everything is in one subdirectory in an archive)"""
    common_prefix = None
    for path in paths:
        prefix, rest = split_leading_dir(path)
        if not prefix:
            return False
        elif common_prefix is None:
            common_prefix = prefix
        elif prefix != common_prefix:
            return False
    return True

def untar_file(filename, location):
    if not os.path.exists(location):
        os.makedirs(location)
    if filename.lower().endswith('.gz') or filename.lower().endswith('.tgz'):
        mode = 'r:gz'
    elif filename.lower().endswith('.bz2') or filename.lower().endswith('.tbz'):
        mode = 'r:bz2'
    elif filename.lower().endswith('.tar'):
        mode = 'r'
    else:
        logger.error('Cannot determine compression type for file %s' % filename)
        mode = 'r:*'
    tar = tarfile.open(filename, mode)
    try:
        # note: python<=2.5 doesnt seem to know about pax headers, filter them
        leading = has_leading_dir([
            member.name for member in tar.getmembers()
            if not member.name.startswith('.') and member.name != 'pax_global_header'
        ])
        for member in tar.getmembers():
            fn = member.name
            if fn == 'pax_global_header':
                continue
            if leading:
                fn = split_leading_dir(fn)[1]
            path = os.path.join(location, fn)
            if member.isdir():
                if not os.path.exists(path):
                    os.makedirs(path)
            else:
                try:
                    fp = tar.extractfile(member)
                except (KeyError, AttributeError):
                    e = sys.exc_info()[1]
                    # Some corrupt tar files seem to produce this
                    # (specifically bad symlinks)
                    logger.error('In the tar file %s the member %s is invalid: %s'
                                  % (filename, member.name, e))
                    continue
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                destfp = open(path, 'wb')
                try:
                    shutil.copyfileobj(fp, destfp)
                finally:
                    destfp.close()
                fp.close()
                # note: configure ...etc
                os.chmod(path, member.mode)
                # note: the file timestamps should be such that asdl_c.py is not invoked.
                os.utime(path, (member.mtime, member.mtime))
    finally:
        tar.close()

def extract_downloadfile(content_type, download_file, target_dir):
    logger.info("Extracting %s into %s" % (os.path.basename(download_file), target_dir))
    if is_gzip(content_type, download_file):
        untar_file(download_file, target_dir)
        return True
    else:
        logger.error("Cannot determine archive format of %s" % download_file)
        return False

def is_installed(pkg):
    return os.path.isdir(os.path.join(PATH_PYTHONS, pkg.name))

def path_to_fileurl(path):
    path = os.path.normcase(os.path.abspath(path))
    url = urlquote(path)
    url = url.replace(os.path.sep, '/')
    url = url.lstrip('/')
    return 'file:///' + url

def fileurl_to_path(url):
    assert url.startswith('file:'), ('Illegal scheme:%s' % url)
    url = '/' + url[len('file:'):].lstrip('/')
    return urlunquote(url)

def to_str(val):
    if not PY3K:
        # python2
        if isinstance(val, unicode):
            return val.encode("utf-8")
        return val
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return val

def is_str(val):
    if not PY3K:
        # python2
        return isinstance(val, basestring)
    # python3
    return isinstance(val, str)

def is_sequence(val):
    if is_str(val):
        return False
    return (hasattr(val, "__getitem__") or hasattr(val, "__iter__"))


#-----------------------------
# class
#-----------------------------
class ShellCommandException(Exception):
    """General exception during shell command"""

class Subprocess(object):
    def __init__(self, log=None, cwd=None, verbose=False, debug=False):
        self._log = log
        self._cwd = cwd
        self._verbose = verbose
        self._debug = debug

    def chdir(self, cwd):
        self._cwd = cwd

    def shell(self, cmd):
        if self._debug:
            logger.log(cmd)
        if is_sequence(cmd):
            cmd = ''.join(cmd)
        if self._log:
            if self._verbose:
                cmd = "(%s) 2>&1 | tee '%s'" % (cmd, self._log)
            else:
                cmd = "(%s) >> '%s' 2>&1" % (cmd, self._log)
        returncode = subprocess.call(cmd, shell=True, cwd=self._cwd)
        if returncode:
            raise ShellCommandException('%s: failed to `%s`' % (returncode, cmd))

    def call(self, cmd):
        if is_str(cmd):
            cmd = shlex.split(cmd)
        if self._debug:
            logger.log(cmd)

        fp = ((self._log and open(self._log, 'a')) or None)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self._cwd)
        while p.returncode is None:
            while any(select.select([p.stdout], [], [])):
                line = to_str(p.stdout.readline())
                if not line:
                    break
                if self._verbose:
                    logger.log(line.strip())
                if fp:
                    fp.write(line)
                    fp.flush()
            p.poll()
        if fp:
            fp.close()
        return p.returncode

    def check_call(self, cmd):
        returncode = self.call(cmd)
        if returncode:
            raise ShellCommandException('%s: failed to `%s`' % (returncode, cmd))

class Package(object):
    def __init__(self, version, type):
        type = type.lower()
        if type == 'cpython':
            tag = 'CPython'
        elif type == 'stackless':
            tag = 'Stackless'
        elif type == 'pypy':
            tag = 'PyPy'
        elif type == 'pypy3':
            tag = 'PyPy3'
        elif type == 'jython':
            tag = 'Jython'
        else:
            raise ValueError('invalid type: %s' % type)
        self.type = type
        self.tag = tag
        self.version = version

    @property
    def name(self):
        return '%s-%s' % (self.tag, self.version)

class Link(object):
    def __init__(self, url):
        self._url = url

    @property
    def filename(self):
        url = self._url
        url = url.split('#', 1)[0]
        url = url.split('?', 1)[0]
        url = url.rstrip('/')
        name = posixpath.basename(url)
        assert name, ('URL %r produced no filename' % url)
        return name

    @property
    def base_url(self):
        return posixpath.basename(self._url.split('#', 1)[0].split('?', 1)[0])

class Version(object):
    """version compare
    """
    def __init__(self, v):
        self._version = v
        self._p = self._parse_version(v)

    def __lt__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p < o

    def __le__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p <= o

    def __eq__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p == o

    def __ne__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p != o

    def __gt__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p > o

    def __ge__(self, o):
        if is_str(o):
            o = self._parse_version(o)
        return self._p >= o

    def _parse_version(self, s):
        """see pkg_resouce.parse_version
        """
        component_re = re.compile(r'(\d+ | [a-z]+ | \.| -)', re.VERBOSE)
        replace = {'pre':'c', 'preview':'c','-':'final-','rc':'c','dev':'@'}.get

        def _parse_version_parts(s):
            for part in component_re.split(s):
                part = replace(part,part)
                if not part or part=='.':
                    continue
                if part[:1] in '0123456789':
                    yield part.zfill(8)    # pad for numeric comparison
                else:
                    yield '*'+part
            yield '*final'  # ensure that alpha/beta/candidate are before final

        parts = []
        for part in _parse_version_parts(s.lower()):
            if part.startswith('*'):
                if part<'*final':   # remove '-' before a prerelease tag
                    while parts and parts[-1]=='*final-': parts.pop()
                # remove trailing zeros from each series of numeric parts
                while parts and parts[-1]=='00000000':
                    parts.pop()
            parts.append(part)
        return tuple(parts)

    def __repr__(self):
        return self._version
