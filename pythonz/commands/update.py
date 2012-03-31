
import os
import sys
from pythonz.basecommand import Command
from pythonz.define import PATH_DISTS, ROOT, PATH_BUILD, PYTHONZ_UPDATE_URL, PYTHONZ_UPDATE_URL_CONFIG, PATH_ETC_CONFIG
from pythonz.log import logger
from pythonz.downloader import Downloader, get_headerinfo_from_url
from pythonz.util import rm_r, extract_downloadfile, Link, is_gzip, Subprocess

class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Update the pythonz to the latest version"
    
    def __init__(self):
        super(UpdateCommand, self).__init__()
        self.parser.add_option(
            '--config',
            dest='config',
            action='store_true',
            default=False,
            help='Update config.cfg.'
        )
    
    def run_command(self, options, args):
        if options.config:
            self._update_config(options, args)
        else:
            self._update_pythonz(options, args)
    
    def _update_config(self, options, args):
        # config.cfg update
        # TODO: Automatically create for config.cfg
        download_url = PYTHONZ_UPDATE_URL_CONFIG
        if not download_url:
            logger.error("Invalid download url in config.cfg. `%s`" % download_url)
            sys.exit(1)
        distname = Link(PYTHONZ_UPDATE_URL_CONFIG).filename
        download_file = PATH_ETC_CONFIG
        try:
            d = Downloader()
            d.download(distname, download_url, download_file)
        except:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)
        logger.log("The config.cfg has been updated.")
    
    def _update_pythonz(self, options, args):
        download_url = PYTHONZ_UPDATE_URL
        headinfo = get_headerinfo_from_url(download_url)
        content_type = headinfo['content-type']
        if not options.master and not options.develop:
            if not is_gzip(content_type, Link(download_url).filename):
                logger.error("content type should be gzip. content-type:`%s`" % content_type)
                sys.exit(1)
        
        filename = "pythonz-master"
        distname = "%s.tgz" % filename
        download_file = os.path.join(PATH_DISTS, distname)
        try:
            d = Downloader()
            d.download(distname, download_url, download_file)
        except:
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
        logger.info("The pythonz has been updated.")

UpdateCommand()

