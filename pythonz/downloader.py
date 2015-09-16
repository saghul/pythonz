import sys
from mmap import mmap, PROT_READ
from hashlib import sha256

from pythonz.util import PY3K
from pythonz.log import logger

if PY3K:
    from urllib.request import Request, urlopen, urlretrieve
else:
    from urllib import urlretrieve
    from urllib2 import urlopen, Request


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


class DownloadError(Exception):
    """Exception during download"""


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
    def fetch(cls, url, filename):
        b = ProgressBar()
        try:
            urlretrieve(url, filename, b.reporthook)
            sys.stdout.write('\n')
        except IOError:
            sys.stdout.write('\n')
            raise DownloadError('Failed to fetch %s from %s' % (filename, url))


def validate_sha256(filename, sha256sum):
    if sha256sum is not None:
        with open(filename, 'rb') as f, mmap(f.fileno(), 0, prot=PROT_READ) as m:
            return sha256(m).hexdigest() == sha256sum
    else:
        logger.warning('sha256sum unavailable, skipping verification.\nMake '
                       "sure that the server you're downloading from is trusted")
        return True
