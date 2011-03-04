import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

def SpawnInterfaceManager(**kwargs):
	application_window = QtGui.QApplication([])
	new_interface_manager = InterfaceManager(**kwargs)
	new_interface_manager.show()
	application_window.exec_()
	return new_interface_manager

class InterfaceManager(QtGui.QWidget):
	payload_items = []

	def __init__(self, uploader = None, logger = None, application_title=None, application_logo = None):
		super(InterfaceManager, self).__init__()
		self.application_logo = application_logo
		self.application_title = application_title
		self.upload_manager = uploader
		self.logger = logger
		self.initialise_userinterface()
		self.populate_payload()


	def initialise_userinterface(self):
		## create the main vertical box
		vbox_main = QtGui.QVBoxLayout()
		vbox_main.addStretch(1)

		vbox_header = QtGui.QVBoxLayout()
		hbox_header = QtGui.QHBoxLayout()
		if self.application_logo :
			pixmap_header_logo = QtGui.QPixmap( self.application_logo )
			label_header_logo = QtGui.QLabel(self)
			label_header_logo.setPixmap( pixmap_header_logo )
			hbox_header.addWidget( label_header_logo )

		self.label_application_title = QtGui.QLabel()
		self.label_application_title.setText( str( self.application_title ) )
		hbox_header.addWidget( self.label_application_title )

		button_config = QtGui.QPushButton("Start")
		self.connect(button_config, QtCore.SIGNAL('clicked()'), self.button_config_clicked )
		hbox_header.addWidget(button_config)

		vbox_header.addLayout( hbox_header )

		hr = QtGui.QFrame()
		hr.setFrameShape( QtGui.QFrame.HLine )
		vbox_header.addWidget( hr )

		vbox_main.addLayout( vbox_header )


		vbox_host_chooser = QtGui.QVBoxLayout()
		groupbox_host_chooser = QtGui.QGroupBox("Choose remote host")
		groupbox_host_chooser.setFlat(True)
		hbox_groupbox_items = QtGui.QHBoxLayout()
		self.combo_host_chooser = QtGui.QComboBox(self)
		self.populate_host_chooser(self.combo_host_chooser, [hostname for hostname,hostdata in self.upload_manager.hosts.items()] )
		self.connect(self.combo_host_chooser, QtCore.SIGNAL('activated(QString)'), self.combo_host_chooser_activated)
		hbox_groupbox_items.addWidget( self.combo_host_chooser )
		groupbox_host_chooser.setLayout(hbox_groupbox_items)
		vbox_host_chooser.addWidget(groupbox_host_chooser)

		hr = QtGui.QFrame( )
		hr.setFrameShape( QtGui.QFrame.HLine )
		vbox_host_chooser.addWidget(hr)
		vbox_main.addLayout( vbox_host_chooser )

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
		self.setFocus()
		self.setWindowTitle('Image Uploader')


	##################
	## Events
	def combo_host_chooser_activated(self):
		pass

	def button_config_clicked(self):
		pass

	def button_ok_clicked(self):
		for item in self.payload_items :
			widget = item['widget_progress']
			if widget.timer.isActive():
				self.logger.info("Stopping Widget %s.timer" % widget)
				widget.timer.stop()
#				widget.button.setText('Start')
			else:
				self.logger.info("Starting Widget %s.timer" % widget)
				widget.timer.start(10, widget)
#				widget.button.setText('Stop')

		self.upload_manager.deliver_payload(
			progress_callback = self.progress_callback,
			completed_callback = self.completed_callback
		)

	def button_cancel_clicked(self):
		self.close()

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
	def start(self):
		pass

	def exit(self):
		pass

	def notify_bubble(self, icon, msg):
		os.popen("notify-send --icon=%s %s" % (icon,msg) )

	def populate_host_chooser(self, widget, hosts):
		for host in hosts :
			widget.addItem(host)

	def set_upload_manager(self, manager):
		self.upload_manager = manager

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
		print len(string_payload_item)
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
	def __init__(self, *args, **kwargs):
		super(PayloadItemProgressBar, self).__init__(*args, **kwargs)

	def initialise_userinterface(self):
		pass


class PayloadItemProgressBar(QtGui.QProgressBar):
	def __init__(self, *args, **kwargs):
		super(PayloadItemProgressBar, self).__init__(*args, **kwargs)
		self.timer = QtCore.QBasicTimer()
		self.step = 0

	def set_step(self, value):
		self.step = value

	def timerEvent(self, event):
		if self.step >= 100:
			self.timer.stop()
			return
#		self.step = self.step + 1
		self.setValue(self.step)

