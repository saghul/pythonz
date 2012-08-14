
import urllib
import urllib2
import sys

from pythonz.exceptions import DownloadError


class ProgressBar(object):
    def __init__(self, out=sys.stdout):
        self._term_width = 79
        self._out = out

    def update_line(self, current):
        num_bar = int(current / 100.0 * (self._term_width - 5))
        bars = u'#' * num_bar
        spaces = u' ' * (self._term_width - 5 - num_bar)
        percentage = u'%3d' % int(current) + u'%\r'
        return bars + spaces + u' ' + percentage

    def reporthook(self, blocknum, bs, size):
        current = (blocknum * bs * 100) / size
        if current > 100:
            current = 100
        self._out.write(self.update_line(current))
        self._out.flush()

    def finish(self):
        self._out.write(self.update_line(100))
        self._out.flush()


class HEADRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


class Downloader(object):

    @classmethod
    def read(cls, url):
        try:
            r = urllib.urlopen(url)
        except IOError:
            raise DownloadError('Failed to fetch %s' % url)
        else:
            return r.read()

    @classmethod
    def read_head_info(cls, url):
        try:
            req = HEADRequest(url)
            res = urllib2.urlopen(req)
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
            urllib.urlretrieve(url, filename, b.reporthook)
            sys.stdout.write('\n')
        except IOError:
            sys.stdout.write('\n')
            raise DownloadError('Failed to fetch %s from %s' % (filename, url))


