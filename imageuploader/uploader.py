import os
import sys
import re
import random
import string
import poster
import logging
import urllib2
import ConfigParser


class UploadManager:
	profiles = {}
	files = []
	template_tags = {
		"username"		: lambda x,y: ''.join (random.choice (string.letters) for ii in range (len(y) + 1)),
		"filename"		:	lambda x,y: os.path.abspath(x),
		"title"				: lambda x,y: os.path.split(x)[1],
	}
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
	## Tools
	def fill_template (self,query,file):
		"""
			Replaces placeholders with evaluated function results
		"""
		output = None
		tags = self.template_tags
		query = re.sub("\$","",query)
		if query in tags.keys() :
			output = tags[query](file,query)
			self.logger.info("Replacing template tag [%s] with [%s]" % (query, output) )

		return output

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
			Iterates through self.list_images and does the following :
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

	def progress_callback(self, param, current, total):
		"""
			Used to update the progress bars,
			usually called by the delegated object, which is the upload-manager
		"""
		if hasattr(param,'name') and param.name =="image" and self.item_process_callback :
			if hasattr(param, "filename"):
				self.logger.info("Uploading [ %s ] to %s [ %s/%s ]" % (param.filename, self.target_host.get('host', 'host_url'), current, total))
				self.item_process_callback(param.filename,current, total)

	def deliver_payload(self, progress_callback = None, completed_callback=None):
		"""
			Begins the upload process
		"""
		self.logger.info("Beging payload delivery to remote host: %s, payload-items: %s" % (
				self.target_host.get('host', 'host_url'),
				str(self.list_images)
			)
		)

		self.item_process_callback = progress_callback
		self.item_complete_callback = completed_callback

		for image in self.list_images :
			output = self.upload_file( image )
			self.item_complete_callback(image, output)

	def upload_file(self, file_path = None):
		""" Function doc """
		target = self.target_host

		host = target("host","host_url")
		upload_url = target("host","upload_url")
		data = target._sections["form"].copy()

		self.logger.info("Beginning upload of [ %s ] to [ %s ]" % (file_path,self.target_host))

		for key,value in data.iteritems():
			if "$" in value :
				new_value = self.fill_template(value, file_path)
				if(new_value==None):
					self.logger.error("Could not find template tag : %s" % value)
				else:
					data[key] = new_value

		data[target["imagefield"]] = open(file_path,"rb")

		self.logger.info("Uploading with formdata [ %s ]" % data )
		datagen, headers = poster.encode.multipart_encode(data, cb=self.progress_callback)

		self.logger.info("Building request object")
		request = urllib2.Request(upload_url, datagen, headers)

		self.logger.info("Sending formdata")
		response = urllib2.urlopen(request).read()

		self.logger.info("Searching response for imageID")
		match_obj = re.search( target["needle"], response )

		if match_obj != None :
			image_id = match_obj.group('image_id')
			if image_id != None :
				self.logger.info("imageID : %s" % image_id)
				url = target["show_url"] % image_id
				return url
			else :
				self.logger.error("There was an error uploading the image.")
				self.logger.warn("Page returned data, but could not find image_id.")
				self.logger.debug(match_obj.groups())
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

