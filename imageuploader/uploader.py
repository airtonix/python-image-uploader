import os
import sys
import re
import random
import string
import poster
import logging
import urllib2
import ConfigParser

from .utils import merge

class UploadManager:
	profiles = {}
	files = []

	target_host = None

	def __init__(self, parent = None, files = None):
		self.parent = parent
		self.logger = self.parent.logger
		self.files = self.process_payload(files)

		poster.streaminghttp.register_openers()

		self.logger.info("Loading configuration files")
		self.load_config()

		# find the default target host
		for name, data in self.profiles.items():
			if data.has_section('host') and data.get('host', 'is_default'):
				self.target_host = data
				self.logger.info("Default Config is : %s" % data.get('host', 'name') )
				break

	####################
	## Methods
	def load_config(self):
		config_path = self.parent.configuration_path
		for config_file in os.listdir(config_path):
			self.logger.info("Loading configuration file : %s" % config_file)
			if not config_file in self.profiles.keys() :
				config = ConfigParser.RawConfigParser()
				config.read( os.path.join(config_path, config_file) )
				self.profiles[ config_file ] = config


	def process_payload(self, payload_items = None):
		"""
			Iterates through self.files and does the following :
				1. converts the path to an absolute path
		"""
		if not payload_items:
			return None

		output = []
		files_count = len(payload_items)
		if files_count > 0:
			for index in range(0, files_count ) :
				item = payload_items[index]
				absolute_path = os.path.abspath( os.path.expanduser(item) )
				output.append(absolute_path)

		return output

	def deliver_payload(self, callback_item_beforestart=None, callback_item_progress = None, callback_item_completed = None):
		"""
			Begins the upload process
		"""
		self.logger.info("Beging payload delivery to remote host: %s, payload-items: %s"  % (
				self.target_host.get('host', 'host_url'),
				str(self.files)
			)
		)

		self.callback_item_beforestart = callback_item_beforestart
		self.callback_item_progress = callback_item_progress
		self.callback_item_completed = callback_item_completed

		for image in self.files :

			try:
				self.callback_item_beforestart( image )
			except:
				pass

			try:
				output = self.upload_file( image )
			except:
				pass

			try:
				self.callback_item_completed(image, output)
			except:
				pass

	def upload_file(self, file_path = None):
		""" Function doc """
		target = self.target_host

		host = target.get("host","host_url")
		upload_url = target.get("host","upload_url")
		data = target._sections["form"].copy()
		imagefield_name = target.get("host","imagefield")
		result_remote_url_regex = re.compile(target.get("host","needle"))
		result_remote_url = target.get("host", "show_url")

		self.logger.info("Processing Template Tags")
		meta = {
			"filepath"	: file_path,
			"length"		: target.get("host", "random_length"),
		}

		for key,value in data.iteritems():
			new_value = None
			if "$" in value :
				new_value = self.parent.tag_manager.get_tag( **merge(meta, { "tag": value}) )
				if new_value :

					data[key] = new_value

		self.logger.info("Beginning upload of [ %s ] to [ %s ]" % (file_path,upload_url) )

		data[imagefield_name] = open(file_path,"rb")

		self.logger.info("Uploading with formdata [ %s ]" % data )
		datagen, headers = poster.encode.multipart_encode(data, cb = self.callback_item_progress)

		self.logger.info("Building request object : data\n %s")
		request = urllib2.Request(upload_url, datagen, headers)

		self.logger.info("Sending formdata")
		response = urllib2.urlopen(request).read()

		self.logger.info("Searching response for imageID")
		match_obj = result_remote_url_regex.search( response )

		if match_obj != None :
			image_id = match_obj.group('image_id')
			if image_id != None :
				url = result_remote_url % image_id
				self.logger.info("imageID : %s" % image_id)
				self.logger.info("remoteurl : %s" % url)
				return url
			else :
				self.logger.error("There was an error uploading the image. Page returned data, but could not find image_id.")
				self.logger.info(match_obj.groups())
		else :
			self.logger.error("There was an error uploading the image.")
			self.logger.info("Did not return match id")

	####################
	## Get/Set
	#TODO: Convert to proper python properties
	def set_logger(self, logger_object):
		self.logger = logger_object

	def set_interface_manager(self, manager):
		self.interface_manager = manager

	def set_target_host(self, host):
		self.target_host = host

	def get_upload_urls(self):
		pass

