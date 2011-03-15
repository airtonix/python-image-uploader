import os
from PySide import QtCore,QtGui
#####################
##
## Application Logo
##
class ApplicationLogo( QtGui.QLabel):
	"""
		Style IDs
			#application-logo
	"""
	_filename = ""

	def __init__(self,filename = None):
		super(ApplicationLogo, self).__init__()
		self.image = filename
		self.setObjectName('application-logo')

	def set_image(self, filename):
		"""
			image@Property : Set
			Make the QPixmap use the filename for the image.
				@ filename : absolute pathname to the image
		"""

		self._image_path = filename
		pixmap = QtGui.QPixmap( filename )
		self.setPixmap( pixmap )

	def get_image(self):
		"""
			image@Property : Get
			Return the path to the current filename being used.
		"""
		return self._filename
	image = property(get_image, set_image)

#####################
##
## Application Header Row
##
class ApplicationHeader( QtGui.QFrame ):
	"""
		Style IDs
			#header
			#header-inner
			#application-title
	"""
	str_required_variable_message = "This Class requires two variables : 'application_title' and 'application_logo_path'"

	def __init__(self, application_title=None, application_logo_path=None):
		"""
			Interface Construction :
				Build the Header Area.
		"""
		super(ApplicationHeader, self).__init__()

		self.setObjectName('header')
		layout = QtGui.QHBoxLayout()
		layout.setObjectName('header-inner')
		self.application_logo = ApplicationLogo( filename = application_logo_path )
		layout.addWidget( self.application_logo , QtCore.Qt.AlignLeft)

		self.label_application_title = QtGui.QLabel()
		self.label_application_title.setObjectName('application-title')
		layout.addWidget( self.label_application_title , QtCore.Qt.AlignLeft)
		try :
			self.label_application_title.setText( str( application_title ) )
		except:
			raise ValueError, "ApplicationHeader missing argument: application_title.\n %s" % self.str_required_variable_message

		self.setLayout(layout)

		self.setSizePolicy(
			QtGui.QSizePolicy(
				QtGui.QSizePolicy.Fixed,
				QtGui.QSizePolicy.Fixed))


		###############################
		## GET/SET for application_title
		def set_application_title(self, value):
			self._application_title = value
			self.label_application_title.setText(value)

		def get_application_title(self):
			return self._application_title

		self.application_title = property(get_application_title, set_application_title)

		###############################
		## GET/SET for application_logo
		def set_application_logo(self, value):
			self._application_logo_path = value
			pixmap_logo = QtGui.QPixmap( self._application_logo_path )
			self.label_application_logo.setPixmap( pixmap_logo )

		def get_application_logo(self):
			"""
				Returns the path for the current application logo  pixmap
			"""
			return self._application_logo_path

		self.application_logo = property(get_application_logo, set_application_logo)


#####################
##
## PayloadItem Item Widget
##
class PayloadItemWidget( QtGui.QFrame ):
	"""
		Style IDs
			#payload-item
			#payload-item-inner
			#payload-item-label
			#payload-item-label-inner
			#payload-item-label-filename
			#payload-item-label-remote-url
	"""
	def __init__(self, text=None, pixmap_uri=None):
		super(PayloadItemWidget, self).__init__()
		self.setObjectName('payload-item')
		self.layout = QtGui.QHBoxLayout()
		self.layout.setObjectName('payload-item-inner')

		self.icon = QtGui.QLabel()
		self.setIcon( pixmap_uri )
		self.layout.addWidget( self.icon )

		row_label_container = QtGui.QFrame()
		row_label_container.setObjectName('payload-item-label')
		row_label_box = QtGui.QVBoxLayout()
		row_label_box.setObjectName('payload-item-label-inner')

		self.label_filename = QtGui.QLabel()
		self.label_filename.setObjectName('payload-item-label-filename')
		self.label_filename.setText(text)
		row_label_box.addWidget( self.label_filename )

		self.progressbar = PayloadItemProgressBar()
		self.progressbar.setFile(filename = pixmap_uri)
		row_label_box.addWidget( self.progressbar )
		row_label_container.setLayout( row_label_box )

		self.label_url = QtGui.QLabel()
		self.label_url.setObjectName('payload-item-label-remote-url')
		self.label_url.setText("")
		self.label_url.setOpenExternalLinks(True)
		row_label_box.addWidget( self.label_url )

		self.layout.addWidget( row_label_container )
		self.setLayout( self.layout )

	def progress(self,value):
		self.progressbar.progressbar.setValue(value)

	def get_label_name(self):
		return self.label_filename.text()

	def set_label_name(self, value):
		self.label_filename.setText(value)

	def get_label_url(self):
		return self.label_url.text()

	def set_label_url(self, value):
		self.label_url.setText("<a href='%(url)s'>%(url)s</a>" % { "url":value })


	def setIcon(self, uri):
		pixmap = QtGui.QPixmap( uri )
		if pixmap and pixmap.width > 64 :
			pixmap = pixmap.scaledToWidth(64)
		self.icon.setPixmap( pixmap )

	def get_progress(self):
		return self.progressbar.progressbar.maximum()

	def set_progress(self, value):
		if value >= self.progressbar.progressbar.maximum() :
			value = self.progressbar.progressbar.maximum()
		self.progressbar.progressbar.setValue(value)


class PayloadItemProgressBar(QtGui.QFrame):
	"""
		Style IDS
			#payload-item-progress
			#payload-item-progress-inner
			#payload-item-progress-bar
	"""
	def __init__(self, *args, **kwargs):
		super(PayloadItemProgressBar, self).__init__(*args, **kwargs)
		self.setObjectName('payload-item-progress')
		self.layout = QtGui.QHBoxLayout()
		self.layout.setObjectName('payload-item-progress-inner')
		self.step = 0
		self.progressbar = QtGui.QProgressBar()
		self.progressbar.setObjectName('payload-item-progress-bar')
		self.layout.addWidget(self.progressbar)
#		self.button = QtGui.QPushButton("Start")
#		layout.addWidget(self.button)
		self.setLayout(self.layout)

	def setFile(self, filename):
		filesize = os.path.getsize(filename)
		self.progressbar.setMinimum(0)
		self.progressbar.setMaximum(int(filesize))



#####################
##
##  Payload Item List View
##   subclassed QWidgetList

class PayloadListWidget( QtGui.QFrame ):
	"""
		Stylesheet IDs
			payload-list
	"""
	def __init__(self,*args, **kwargs):
		super(PayloadListWidget, self).__init__()
		self.setObjectName('payload-list')
		self.setSizePolicy(
			QtGui.QSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding))

		self.layout = QtGui.QVBoxLayout()
		self.layout.setObjectName('payload-list-inner')
		self.setLayout( self.layout )


	def populate(self, list_items = None):
		"""
			Populates the list with interface representations of the
			imagefiles to be uploaded.

			Relies on the parent object having a property pointing at
			the upload managers "files" property, which contains a
			list of pathnames to imagefiles.

				> parent.upload_manager.files(list)
		"""
		self.payload = {}
		if list_items and len(list_items) > 0 :
			for item in list_items:
				self.add_item( item )

	def add_item(self, item):
		widget = PayloadItemWidget(
			text = item,
			pixmap_uri = item
		)
		self.payload[item] = widget
		self.layout.addWidget(widget)

	def get_item(self, filename):
		if filename in self.payload.keys():
			return self.payload[ filename ]
		else:
			return None

	def count(self):
		return len(self.payload)

	def items(self):
		for filename, item in self.payload.items():
			yield item

