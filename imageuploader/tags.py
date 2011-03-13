import os
import random, string
from .utils import merge

class TagManager:
	tags = {}

	def __init__(self,parent= None, tags=None):
		if not parent or not hasattr(parent, "logger") :
			raise AttributeError, "TagManager requires a parent association to an object which contains a 'logger' member object of type Logging."
			exit()

		self.parent = parent
		default_tags = {
			"user"				: lambda **kwargs: ''.join (random.choice (string.letters) for ii in range (len(kwargs['length']) + 1)),
			"filename"		:	lambda **kwargs: os.path.basename(kwargs['filepath'])[0],
			"title"				: lambda **kwargs: os.path.split(kwargs['filepath'])[1],
		}

		if tags :
			self.tags = merge(default_tags, tags)
		else:
			self.tags = default_tags

	def load_tags(self, filepath=None, tags=None):
		if tags :
			if isinstance(dict, tags):
				self.parent.logger.info("Loading tags from dictionary input.")
				pass

			elif isinstance(list, tags):
				self.parent.logger.info("Loading tags from list input.")
				pass

		elif filename :
			self.parent.logger.info("Loading tags from list input.")

		else :
			self.parent.logger.error("No source provided to load tags from.")

	def get_tag(self, **kwargs):
		try :
			tag = kwargs['tag'].lower().replace("$", "")
		except:
			AttributeError, "TagManager.get_tag requires a keyword argument 'tag' "
			exit()

		self.parent.logger.info("Searching for Tag : %s" % tag)
		if tag in self.tags.keys():
			result = self.tags[tag](**kwargs)
			self.parent.logger.info("Tag [ %s ] converted to  : %s" % (tag,result))
			return result
		else:
			return None

	def set_tag(self,tagname,value):
		self.tags[tagname] = value

	tag = property(get_tag, set_tag)


class Tag:
	_name = None
	_value = None

	def __init__(self, name = None, value = None):
		self.name = name
		self.value = value

	def get_name(self):
		return self._name
	def set_name(self,value):
		self._name = value
	name = property(get_name, set_name)

	def get_value(self):
		return self._value
	def set_value(self,value):
		self._value = value
	value = property(get_value, set_value)

