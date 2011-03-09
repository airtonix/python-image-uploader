from PySide import QtCore,QtGui

#####################
##
## Application Logo
##
class ApplicationLogo( QtGui.QLabel):
	_filename = ""

	def __init__(self,filename = None):
		super(ApplicationLogo, self).__init__()
		self.image = filename

	def set_image(self, filename):
		"""
			image@Property : Set
			Make the QPixmap use the filename for the image.
				@ filename : absolute pathname to the image
		"""
		print "Setting Application Icon as : %s" % filename
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
class ApplicationHeader( QtGui.QWidget ):
	str_required_variable_message = "This Class requires two variables : 'application_title' and 'application_logo_path'"

	def __init__(self, application_title=None, application_logo_path=None):
		"""
			Interface Construction :
				Build the Header Area.
		"""
		super(ApplicationHeader, self).__init__()
		layout = QtGui.QHBoxLayout()
		self.application_logo = ApplicationLogo( filename = application_logo_path )
		layout.addWidget( self.application_logo , QtCore.Qt.AlignLeft)

		try :
			self.application_title = application_title
			self.label_application_title = QtGui.QLabel()
			self.label_application_title.setText( str( application_title ) )
			layout.addWidget( self.label_application_title , QtCore.Qt.AlignLeft)
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
class PayloadItemWidget( QtGui.QWidget ):

	def __init__(self, text=None, pixmap_uri=None):
		super(PayloadItemWidget, self).__init__()
		self.layout = QtGui.QHBoxLayout()

		print pixmap_uri

		self.icon = QtGui.QLabel()
		self.setIcon( pixmap_uri )
		self.layout.addWidget( self.icon )

		row_label_container = QtGui.QWidget()
		row_label_box = QtGui.QVBoxLayout()

		self.label = QtGui.QLabel()
		self.label.setText(text)
		row_label_box.addWidget( self.label )

		self.progressbar = PayloadItemProgressBar()
		row_label_box.addWidget( self.progressbar )
		row_label_container.setLayout( row_label_box )

		self.layout.addWidget( row_label_container )

		self.setLayout( self.layout )

	def setIcon(self, uri):
		pixmap = QtGui.QPixmap( uri )
		if pixmap and pixmap.width > 64 :
			pixmap = pixmap.scaledToWidth(64)
		self.icon.setPixmap( pixmap )


	def setText(self, text):
		self.label.setText(text)

	def setProgress(self, value):
		self.progressbar.set_step(value)

#	def paintEvent(self,event):
#		pixmap = self.pixmap_icon
#		painter = QtGui.QPainter(self)
#		painter.drawText(self.size//2,self.size//2,str(self.text))

class PayloadItemProgressBar(QtGui.QProgressBar):
	def __init__(self, *args, **kwargs):
		super(PayloadItemProgressBar, self).__init__(*args, **kwargs)
		self.timer = QtCore.QBasicTimer()
		self.step = 0

	def setStep(self, value):
		self.step = value

	def startTimer(self):
		self.timer.start()

	def stopTimer(self):
		self.timer.stop()

	def timerEvent(self, event):
		if self.step >= 100:
			self.stop_timer()
			return
		self.setValue(self.step)

#####################
##
##  Payload Item List View
##   subclassed QWidgetList

class PayloadListWidget( QtGui.QWidget ):
	def __init__(self,*args, **kwargs):
		super(PayloadListWidget, self).__init__()

#		self.setBackgroundRole( QtGui.QPalette.Dark )
#		self.scrollarea = QtGui.QScrollArea
#		self.addLayout( self.scrollarea )

		self.setSizePolicy(
			QtGui.QSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding))

		self.layout = QtGui.QVBoxLayout()
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
		if list_items and len(list_items) > 0 :
			for item in list_items:
				self.add_item( item )

	def add_item(self, item):
		self.layout.addWidget( PayloadItemWidget(
			text = item,
			pixmap_uri = item
		) )

	def items(self):
		for index in range(self.count()):
			yield self.item(index)

