
import os
import sys

from pythonz.basecommand import Command
from pythonz.define import PATH_DISTS, ROOT, PATH_BUILD, PYTHONZ_UPDATE_URL
from pythonz.downloader import Downloader
from pythonz.exceptions import DownloadError
from pythonz.log import logger
from pythonz.util import rm_r, extract_downloadfile, Link, unlink, Subprocess


class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Update pythonz to the latest version"

    def run_command(self, options, args):
        download_url = PYTHONZ_UPDATE_URL
        headinfo = Downloader.read_head_info(download_url)
        content_type = headinfo['content-type']
        filename = "pythonz-latest"
        distname = "%s.tgz" % filename
        download_file = os.path.join(PATH_DISTS, distname)
        # Remove old tarball
        unlink(download_file)
        logger.info("Downloading %s as %s" % (distname, download_file))
        try:
            Downloader.fetch(download_url, download_file)
        except DownloadError:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)

        extract_dir = os.path.join(PATH_BUILD, filename)
        rm_r(extract_dir)
        if not extract_downloadfile(content_type, download_file, extract_dir):
            sys.exit(1)

        try:
            logger.info("Installing %s into %s" % (extract_dir, ROOT))
            s = Subprocess()
            s.check_call([sys.executable, os.path.join(extract_dir,'pythonz_install.py'), '--upgrade'])
        except:
            logger.error("Failed to update pythonz.")
            sys.exit(1)
        logger.info("pythonz has been updated.")

UpdateCommand()

