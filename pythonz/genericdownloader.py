# coding: utf-8

import re
import urllib
import urllib2
import sys
import traceback

from pythonz.log import logger
from pythonz.exceptions import CurlFetchException

class ProgressBar(object):
    def __init__(self, out=sys.stdout):
        self._term_width = 79
        self._out = out

    def update_line(self, current):
        num_bar = int(current / 100.0 * (self._term_width - 5))
        return '#' * num_bar + ' ' * (self._term_width - 5 - num_bar) + \
               u' %3d' % int(current) + u'%\r'

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

class GenericDownloader(object):
    @classmethod
    def can_use(cls):
        return True

    def read(self, url):
        try:
            r = urllib.urlopen(url)
        except:
            logger.log(traceback.format_exc())
            raise CurlFetchException('Failed to fetch.')
        return r.read()

    def readheader(self, url):
        try:
            req = HEADRequest(url)
            res = urllib2.urlopen(req)
        except:
            logger.log(traceback.format_exc())
            raise CurlFetchException('Failed to fetch.')
        if res.code != 200:
            raise CurlFetchException('Failed to fetch.')
        return res.info()

    def fetch(self, url, filename):
        b = ProgressBar()
        try:
            r = urllib.urlretrieve(url, filename, b.reporthook)
            sys.stdout.write('\n')
        except:
            sys.stdout.write('\n')
            logger.log(traceback.format_exc())
            raise CurlFetchException('Failed to fetch.')
