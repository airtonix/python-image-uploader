#!/usr/bin/env python
from __future__ import absolute_import
import os
import sys
import getpass
import argparse
import logging

from lib.Interface import SpawnInterfaceManager, InterfaceManager
from lib.Upload import UploadManager
from lib.tools import assure_path

__author__ = "Zenobius Jiricek"
__author_email__ = "airtonix@gmail.com"
__author_website__ = "airtonix.net"
__application_name__ = "pyImagePoster"
__application_version__ = "0.0.1dev"

conf_path = assure_path( os.path.join( os.getenv("HOME"), '.config', __application_name__) )
log_path = assure_path( os.path.join( os.getenv("HOME"), '.local','share', __application_name__,'logs') )

configuration_file = assure_path( os.path.join(conf_path, "remote_hosts.conf") )

log_file = logging.FileHandler( os.path.join(log_path,"debug.log") )
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file.setFormatter(log_formatter)

logger = logging.getLogger(__application_name__)
logger.addHandler(log_file)
logger.setLevel(logging.INFO)

HEREPATH = os.path.abspath( os.path.dirname(__file__) )

logger.info( "HEREPATH = %s" % HEREPATH)

if __name__ == "__main__" :

	parser = argparse.ArgumentParser(description='Upload images to a remote host.')
	parser.add_argument('--files',
		nargs='*',
		dest='files',
		help='files to upload.')

	args = parser.parse_args()

	if not args.files :
		parser.print_help()
	else:
		upload_manager = UploadManager(
			logger = logger,
			files = args.files,
			configuration_path = conf_path
		)

		interface_manager = SpawnInterfaceManager(
			logger = logger,
			uploader = upload_manager,
			application_title = __application_name__,
			application_logo = os.path.join(HEREPATH, "resources", "icons", "application_logo.png" ),
			configuration_path = conf_path
		)

		interface_manager.show()

