import os
import sys
import re
import random
import string
import poster
import logging
import urllib2



class UploadManager:
	hosts ={
		"imagebin.org" : {
			"default" : True,
			"formdata" : {
				"nickname" : "$username$",
				"title" : "$title$",
				"description" : "$title$",
				"disclaimer_agree" : "Y",
				"Submit" : "Submit",
				"mode" : "add"
			},
			"imagefield" : "image",
			"host_url" : "http://imagebin.org/",
			"upload_url" : "index.php?page=add",
			"needle" : r"""(?i)index.php\?mode=image&id=(?P<image_id>[0-9]+)""",
			"show_url" : lambda id: "http://imagebin.org/%s" % id,
			"file_rules" : lambda file: os.rename(file,file.replace("png","jpg")),
		},

		"localhost"	: {
			"default" : False,
			"formdata" : {
				"user" : "$username$",
			},
			"imagefield" : "image",
			"host_url" : "http://localhost:5000",
			"upload_url" : "/upload_image",
			"needle" : r""".*""",
			"show_url" : lambda str: str,
			"file_rules": lambda file: file,
		}

	}
	template_tags = {
		"username"		: lambda x,y: ''.join (random.choice (string.letters) for ii in range (len(y) + 1)),
		"filename"		:	lambda x,y: os.path.abspath(x),
		"title"				: lambda x,y: os.path.split(x)[1],
	}
	target_host = None

	def __init__(self, files=None, logger = None):
		self.list_images = files
		self.process_payload()
		poster.streaminghttp.register_openers()
		if logger :
			self.logger = logger

		# find the default target host
		for name, data in self.hosts.items():
			if data["default"] :
				self.target_host = data
				break

	####################
	## Tools


	def fill_template (self,query,file):
		""" Function doc """
		output = None
		tags = self.template_tags
		query = re.sub("\$","",query)
		if query in tags.keys() :
			output = tags[query](file,query)
			self.logger.info("Replacing template tag [%s] with [%s]" % (query, output) )

		return output

	####################
	## Methods
	def process_payload(self):
		"""
			Iterates through self.list_images and does the following :
				1. converts the path to an absolute path
		"""
		for index in range(0,len(self.list_images)) :
			item = self.list_images[index]
			absolute_path = os.path.abspath(item)
			self.list_images[index] = absolute_path

	def progress_callback(self, param, current, total):
		if hasattr(param,'name') and param.name =="image" and self.item_process_callback :
			if hasattr(param, "filename"):
				self.logger.info("Uploading [ %s ] to %s [ %s/%s ]" % (param.filename, self.target_host['host_url'], current, total))
				self.item_process_callback(param.filename,current, total)

	def deliver_payload(self, progress_callback = None, completed_callback=None):
		"""
			Begins the upload process
		"""
		self.logger.info("Beging payload delivery to remote host: %s, payload-items: %s" % (self.target_host['host_url'], str(self.list_images) ))

		self.item_process_callback = progress_callback
		self.item_complete_callback = completed_callback

		for image in self.list_images :
			output = self.upload_file( image )
			self.item_complete_callback(image, output)

	def upload_file(self, file_path = None):
		""" Function doc """
		target = self.target_host

		host = target["host_url"]
		upload_url = "%s%s" % (host, target["upload_url"] )
		data = target["formdata"].copy()

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
				url = target["show_url"](image_id)
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

