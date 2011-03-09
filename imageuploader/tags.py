class Taglist:
	tags = {}

	def __init__(self, tags=None):
		self.tags = merge(self.tags, tags)

	def get_tag(self,tagname):
		if tagname in self.tags.keys():
			return self.tags[tagname]
		else:
			return None

	def set_tag(self,tagname,value):
		self.tags[tagname] = value


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
	self.name = property(get_name, set_name)

	def get_value(self):
		return self._value
	def set_value(self,value):
		self._value = value
	self.value = property(get_value, set_value)

