
from pythonz.define import PYTHON_VERSION_URL
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

def get_python_version_url(version):
    return PYTHON_VERSION_URL.get(version)

