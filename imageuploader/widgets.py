from PySide import QtCore,QtGui


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

