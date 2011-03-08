

class UploadImagePreview(QtGui.QWidget):
	"""
		Preview Area, designated as the interface area where upload progress for
		each image is displayed.
		@ parent
			the object for which this widget is attached.
	"""
	payload_items = []
	def __init__(self, parent = None):
		super(UploadImagePreview, self).__init__()
		self = parent
		self.initialise_userinterface()
		self.populate_payload()

	def initialise_userinterface(self):

		self.vbox_payload = QtGui.QVBoxLayout()
		vbox_main.addLayout(self.vbox_payload)

		## create the ok/cancel rowg.e-h
		hbox_footer = QtGui.QHBoxLayout()
		button_ok = QtGui.QPushButton("Start")
		self.connect(button_ok, QtCore.SIGNAL('clicked()'), self.button_ok_clicked )
		hbox_footer.addWidget(button_ok)

		button_cancel = QtGui.QPushButton("Close")
		self.connect(button_cancel, QtCore.SIGNAL('clicked()'), self.button_cancel_clicked )
		hbox_footer.addWidget(button_cancel)
		vbox_main.addLayout( hbox_footer )

		# Add some finishing touches
		self.setLayout( vbox_main )


	##################
	## Events


	##################
	## Methods

	def notify_bubble(self, icon, msg):
		os.popen("notify-send --icon=%s %s" % (icon,msg) )

	def populate_payload(self):
		for item in self.upload_manager.list_images :
			self.create_payload_item( item )

	def create_payload_item(self, payload_item):
		"""
			@payload_item is a string which represents the absolute path to the file
		"""
		self.logger.info("Creating user-interface widget row for payload item : %s " % payload_item)
		hbox_payload_item = QtGui.QHBoxLayout()

		pixmap_payload_thumbnail = QtGui.QPixmap( payload_item )
		label_payload_thumbnail = QtGui.QLabel(self)

		if pixmap_payload_thumbnail.width() > 96 :
			pixmap_payload_thumbnail = pixmap_payload_thumbnail.scaledToWidth(96)

		label_payload_thumbnail.setPixmap( pixmap_payload_thumbnail )
		hbox_payload_item.addWidget( label_payload_thumbnail )

		vbox_payload_item_meta = QtGui.QVBoxLayout()

		label_payload_item_file = QtGui.QLabel(self)
		string_payload_item = payload_item

		if len(string_payload_item)>48 :
			string_payload_item = "%s ... %s" % (payload_item[:21], payload_item[-21:])
		label_payload_item_file.setText( string_payload_item )
		vbox_payload_item_meta.addWidget( label_payload_item_file )


		vbox_payload_item_meta.addWidget( progress_payload_item )

		entry_payload_remoteurl = QtGui.QLineEdit(self)
		vbox_payload_item_meta.addWidget( entry_payload_remoteurl )

		hbox_payload_item.addLayout( vbox_payload_item_meta )

		self.payload_items.append({
			"file" : payload_item,
			"widget_progress" : progress_payload_item,
			"widget_remoteurl" : entry_payload_remoteurl
		})

		self.vbox_payload.addLayout( hbox_payload_item )

