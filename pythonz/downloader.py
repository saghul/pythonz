
from pythonz.define import PYTHON_VERSIONS_URLS
from pythonz.log import logger
from pythonz.curl import Curl
from pythonz.genericdownloader import GenericDownloader


def get_concrete_downloader():
    if Curl.can_use():
        return Curl()
    else:
        return GenericDownloader()

def get_headerinfo_from_url(url):
    c = get_concrete_downloader()
    return c.readheader(url)

class Downloader(object):
    def download(self, msg, url, path):
        logger.info("Downloading %s as %s" % (msg, path))
        c = get_concrete_downloader()
        c.fetch(url, path)

def get_python_version_url(type, version):
    return PYTHON_VERSIONS_URLS[type].get(version)

