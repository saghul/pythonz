
from pythonz.define import PYTHON_VERSIONS_URLS
from pythonz.log import logger
from pythonz.curl import Curl

def get_headerinfo_from_url(url):
    c = Curl()
    return c.readheader(url)

class Downloader(object):
    def download(self, msg, url, path):
        logger.info("Downloading %s as %s" % (msg, path))
        c = Curl()
        c.fetch(url, path)

def get_python_version_url(type, version):
    return PYTHON_VERSIONS_URLS[type].get(version)

