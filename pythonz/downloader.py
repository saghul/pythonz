import sys
import os

from pythonz.util import PY3K
from pythonz.log import logger

if PY3K:
    from urllib.request import Request, urlopen
else:
    from urllib2 import urlopen, Request

try:
    from resumable import urlretrieve, DownloadError, sha256
except ImportError:
    from mmap import mmap as _mmap, ACCESS_READ
    import hashlib
    if PY3K:
        from urllib.request import urlretrieve as _urlretrieve
        mmap = _mmap
    else:
        from contextlib import closing
        mmap = lambda *args, **kwargs: closing(_mmap(*args, **kwargs))
        from urllib import urlretrieve as _urlretrieve

    class DownloadError(Exception):
        """Exception during download"""

    def sha256(filename):
        with open(filename, 'rb') as f:
            with mmap(f.fileno(), 0, access=ACCESS_READ) as m:
                return hashlib.sha256(m).hexdigest()


    def validate_sha256(filename, sha256sum):
        if sha256sum is not None:
            return sha256(filename) == sha256sum
        else:
            logger.warning("sha256sum unavailable, skipping verification.\nMake "
                           "sure that the server you're downloading from is trusted")
            return True


    def urlretrieve(url, filename, reporthook, sha256sum):
        try:
            _urlretrieve(url, filename, reporthook)
            if not validate_sha256(filename, sha256sum):
                raise DownloadError("Corrupted download, the sha256 doesn't match")
        except BaseException:
            os.unlink(filename)
            raise



class ProgressBar(object):
    def __init__(self, out=sys.stdout):
        self._term_width = 79
        self._out = out

    def update_line(self, current):
        num_bar = int(current / 100.0 * (self._term_width - 5))
        bars = '#' * num_bar
        spaces = ' ' * (self._term_width - 5 - num_bar)
        percentage = '%3d' % int(current) + '%\r'
        result = bars + spaces + ' ' + percentage
        if not PY3K:
            # Python 2.x
            return result.decode("utf-8")
        return result

    def reporthook(self, blocknum, bs, size):
        current = (blocknum * bs * 100) / size
        if current > 100:
            current = 100
        self._out.write(self.update_line(current))
        self._out.flush()

    def finish(self):
        self._out.write(self.update_line(100))
        self._out.flush()


class HEADRequest(Request):
    def get_method(self):
        return "HEAD"


class Downloader(object):

    @classmethod
    def read(cls, url):
        try:
            r = urlopen(url)
        except IOError:
            raise DownloadError('Failed to fetch %s' % url)
        else:
            return r.read()

    @classmethod
    def read_head_info(cls, url):
        try:
            req = HEADRequest(url)
            res = urlopen(req)
        except IOError:
            raise DownloadError('Failed to fetch %s' % url)
        else:
            if res.code != 200:
                raise DownloadError('Failed to fetch %s' % url)
            return res.info()

    @classmethod
    def fetch(cls, url, filename, expected_sha256):
        b = ProgressBar()
        try:
            urlretrieve(url, filename, b.reporthook, sha256sum=expected_sha256)
            sys.stdout.write('\n')
        except DownloadError:
            if os.path.exists(filename):
                os.unlink(filename)
            raise
        except IOError:
            sys.stdout.write('\n')
            raise DownloadError('Failed to fetch %s from %s' % (filename, url))
