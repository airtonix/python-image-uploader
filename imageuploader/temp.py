

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
	def get_payload_row(self, filename = None):
		item_row = None

		for item in self.payload_items :
			if item['file'] == filename :
				item_row = item

			if item_row :
				return item_row

		return None

	def completed_callback(self, name, return_data):
		widget_row = self.get_payload_row(filename = name)
		self.update_progress_widget( widget_row['widget_progress'], 100)
		widget_row['widget_remoteurl'].setText(return_data)

	def progress_callback(self, name, current, total):
		widget_row = self.get_payload_row(filename = name)
		if widget_row :
			widget_progress = widget_row['widget_progress']
			step= int( float(current)/float(total)*100 )
			self.update_progress_widget(widget_progress, step)
			self.logger.info("Updating Widget %s [%s/%s](%s)" % (widget_progress, current, total, step ))

	def update_progress_widget(self, widget, value):
		if value > 100 :
			value = 100
		widget.step = value
		widget.setValue( value )

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

		progress_payload_item = PayloadItemProgressBar(self)
		progress_payload_item.setRange(0, 100)
		progress_payload_item.setValue(0)
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


class ConfigWindow(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ConfigWindow, self).__init__()
		self = parent

	def initialise_userinterface(self):
		vbox_main = QtGui.QVBoxLayout()
		vbox_main.addStretch(1)

		hbox_hostname = QtGui.QHBoxLayout()
		self.label_hostname = QtGui.QLabel("Hostname")
		hbox_hostname.addWidget( self.label_hostname )
		self.entry_hostname = QtGui.QLineEdit()
		hbox_hostname.addWidget( self.entry_hostname )
		hr = QtGui.QFrame()
		hr.setFrameShape( QtGui.QFrame.HLine )
		vbox_hostname.addWidget( hr )

		hbox_default = QtGui.QHBoxLayout()
		self.label_default = QtGui.QLabel("Default")
		hbox_default.addWidget( self.label_default )
		self.checkbox_default = QtGui.QCheckBox()
		hbox_default.addWidget( self.entry_default )
		hr = QtGui.QFrame()
		hr.setFrameShape( QtGui.QFrame.HLine )
		vbox_default.addWidget( hr )

		hbox_default = QtGui.QHBoxLayout()
		self.label_default = QtGui.QLabel("Default")
		hbox_default.addWidget( self.label_default )
		self.checkbox_default = QtGui.QCheckBox()
		hbox_default.addWidget( self.entry_default )
		hr = QtGui.QFrame()
		hr.setFrameShape( QtGui.QFrame.HLine )
		vbox_default.addWidget( hr )

