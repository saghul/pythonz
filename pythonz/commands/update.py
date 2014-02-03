
import os
import sys

from pythonz.commands import Command
from pythonz.define import PATH_DISTS, ROOT, PATH_BUILD, PYTHONZ_UPDATE_URL, PYTHONZ_DEV_UPDATE_URL
from pythonz.downloader import Downloader
from pythonz.exceptions import DownloadError
from pythonz.log import logger
from pythonz.util import rm_r, extract_downloadfile, Link, unlink, Subprocess


class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Update pythonz to the latest version"

    def __init__(self):
        super(UpdateCommand, self).__init__()
        self.parser.add_option(
            "--dev",
            dest="dev",
            action="store_true",
            default=False,
            help="Use the development branch."
        )

    def run_command(self, options, args):
        if options.dev:
            download_url = PYTHONZ_DEV_UPDATE_URL
        else:
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
            unlink(download_file)
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)
        except:
            unlink(download_file)
            raise

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

