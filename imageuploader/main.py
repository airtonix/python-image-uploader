#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import string
import getpass
import argparse
import logging

from PySide import QtCore,QtGui


from . import utils
from .uploader import UploadManager
from .widgets import PayloadItemWidget, PayloadListWidget


__author__ = "Zenobius Jiricek"
__author_email__ = "airtonix@gmail.com"
__author_website__ = "airtonix.net"
__application_name__ = "pyImagePoster"
__application_version__ = "0.0.2dev"



#####################
## Application Path
##
application_path = os.path.abspath( os.path.dirname(__file__) )

#####################
## Application Log File Manager
##
configuration_path = utils.assure_path( os.path.join( os.getenv("HOME"), '.config', __application_name__) )
log_path = utils.assure_path( os.path.join( os.getenv("HOME"), '.local','share', __application_name__,'logs') )

log_file = logging.FileHandler( os.path.join(log_path,"debug.log") )
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file.setFormatter(log_formatter)

logger = logging.getLogger(__application_name__)
logger.addHandler(log_file)
logger.setLevel(logging.INFO)

logger.info( "application_path = %s" % application_path)


#####################
##
##	Master Application Object
##
class ImageUploader(QtGui.QApplication):

	def __init__(self, args):
		super(ImageUploader, self).__init__(args)
		parser = argparse.ArgumentParser(description='Upload images to a remote host.')
		parser.add_argument('--files',
			nargs='*',
			dest='files',
			help='files to upload.')

		self.arguments = parser.parse_args()

		self.application_path = application_path
		self.application_title = __application_name__
		self.configuration_path = configuration_path

		self.logger = logger

		self.upload_manager = UploadManager(
			parent = self,
			files = self.arguments.files
		)

		self.mainWindow = MainWindow(self)
		self.mainWindow.setWindowTitle( __application_name__ )

		self.mainWindow.statusBar().showMessage("Ready")


#####################
##
## Top Level Interface Elements
##
class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None, *args):
		super(MainWindow, self).__init__(*args)
		self.parent = parent

		self.centralWidget = QtGui.QWidget()
		self.setCentralWidget(self.centralWidget)

		self.header_row = self.create_header()
		self.footer_row = self.create_footer()
		self.payload_list = PayloadListWidget(self)

		main_layout = QtGui.QGridLayout()
		main_layout.addWidget( self.header_row, 0,0, 1,0, QtCore.Qt.AlignTop)
		main_layout.addWidget( self.payload_list, 1,0, 6,1,QtCore.Qt.AlignTop)
		main_layout.addWidget( self.footer_row, 7,0, 1,0, QtCore.Qt.AlignTop)

		self.centralWidget.setLayout(main_layout)
		self.payload_list.populate( self.parent.upload_manager.files )
		self.setFocus()

	#####################
	##
	## Top Level Application GUI Action Methods
	##
	def exit(self):
		"""
			Stop any operations, and quit the application.
			TODO: implement this.
		"""
		pass

	#####################
	##
	## Top Level Application GUI Creation Methods
	##
	def create_header(self):
		"""
			Interface Construction :
				Build the Header Area.
		"""
		row = QtGui.QWidget()

		layout = QtGui.QHBoxLayout()

		pixmap_header_logo = QtGui.QPixmap( os.path.join(self.parent.application_path, "resources", "icons", "application_logo.png" ) )
		label_header_logo = QtGui.QLabel()
		label_header_logo.setPixmap( pixmap_header_logo )
		layout.addWidget( label_header_logo )

		self.label_application_title = QtGui.QLabel()
		self.label_application_title.setText( str( self.parent.application_title ) )
		layout.addWidget( self.label_application_title , QtCore.Qt.AlignLeft)

		row.setLayout(layout)
		row.setSizePolicy(
			QtGui.QSizePolicy(
				QtGui.QSizePolicy.Fixed,
				QtGui.QSizePolicy.Fixed))
		return row


	def create_footer(self):
		"""
			Interface Construction :
				Build the Footer Area.
		"""
		row = QtGui.QWidget()
		layout = QtGui.QHBoxLayout()

		# Combo drop down menu allowing the user to change the target remote host
		self.combo_host_chooser = QtGui.QComboBox(self)
		self.populate_host_chooser(self.combo_host_chooser, self.parent.upload_manager.profiles )
		self.connect(self.combo_host_chooser, QtCore.SIGNAL('activated(QString)'), self.combo_host_chooser_activated)
		layout.addWidget( self.combo_host_chooser)

		## button to spawn the configuration interface
		pixmap_config_icon = QtGui.QIcon( os.path.join(self.parent.application_path, "resources", "icons", "config.png" ) )
		button_config = QtGui.QPushButton()
		button_config.setFlat(True)
		button_config.setFixedSize(32,32)
		button_config.setIcon(pixmap_config_icon )
		self.connect(button_config, QtCore.SIGNAL('clicked()'), self.button_config_clicked )
		layout.addWidget(button_config, stretch = 0)

		# button to start the upload process
		pixmap_start_delivery_icon = QtGui.QIcon( os.path.join(self.parent.application_path, "resources", "icons", "start_delivery.png" ) )
		button_start_delivery = QtGui.QPushButton()
		button_start_delivery.setFlat(True)
		button_start_delivery.setFixedSize(32,32)
		button_start_delivery.setIcon(pixmap_start_delivery_icon )
		self.connect(button_start_delivery, QtCore.SIGNAL('clicked()'), self.button_start_delivery_clicked )
		layout.addWidget(button_start_delivery, stretch = 0)

		row.setLayout(layout)
		row.setSizePolicy(
			QtGui.QSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding))

		return row

	#####################
	##
	## Auxillary Methods
	##
	def populate_host_chooser(self, widget, profiles):
		"""
			Fills the combo-drop-down menu with profile names to choose.
			TODO: empty the list before filling it.
				@widget: pointer to the widget object
				@profiles : list of profiles
		"""
		for hostname, data in profiles.items() :
			widget.addItem( os.path.splitext(hostname)[0] )

	def get_payload_item(self, filename = None):
		found = False
		item_count = self.payload_view.count()
		print item_count
#		for index in range(0, item_count ) :
#			item = self.payload_view.item(index)
#			print "inspecting %s for %s" % (item, filename)

	def create_payload_item(self, filename):
		"""
			Creates an interface item representing a image to be uploaded
				@filename : the absolute path the imagefile.
		"""
		pixmap_item = QtGui.Pixmap(filename)
		icon_item = IconDisplayItem( filename , pixmap_item )
		return icon_item

	#############################
	##
	## Interface Callback Methods
	##
	def menu_about_clicked(self):
		"""
			Called from them menu system.
			The usual About window
		"""
		QMessageBox.about(self,
			"About %s" % self.parent.application_title,
			"...")

	def combo_host_chooser_activated(self):
		"""
			Called when the dropdown box value is changed.
		"""
		value = self.combo_host_chooser.currentText()
		self.parent.logger.info("Remote Host changed to : %s" % value)
		pass

	def button_start_delivery_clicked(self):
		"""
			start/deliver/begin button.
			Begins the delivery of payload items to designated remote host
		"""
#		for item in self.payload_view.items():
#			widget = item['widget_progress']
#			if widget.timer.isActive():
#				self.parent.logger.info("Stopping Widget %s.timer" % widget)
#				widget.timer.stop()
##				widget.button.setText('Start')
#			else:
#				self.logger.info("Starting Widget %s.timer" % widget)
#				widget.timer.start(10, widget)
##				widget.button.setText('Stop')

		self.parent.upload_manager.deliver_payload(
			callback_item_beforestart = self.callback_payload_item_beforestart,
			callback_item_progress = self.callback_payload_item_progress,
			callback_item_completed = self.callback_payload_item_completed
		)

	def button_config_clicked(self):
		"""
			config button used to access the configuration interface
		"""
		self.parent.logger.info("Configuration Interface requested by user")
		self.config_interface = ConfigWindow(self)
		self.config_interface.show()


	def button_cancel_clicked(self):
		"""
			Stops any delivery process operations
		"""
		self.close()


	def callback_payload_item_beforestart(self, name):
		"""
			Called whenever an image is about to begin uploading.
				@name : the file that was uploaded
		"""
		self.parent.logger.info("About to request payload delivery for %s from upload manager." % name)
		item_widget = self.get_payload_item(filename = name)

#		self.update_progress_widget( item_widget.progressbar, 0)

	def callback_payload_item_completed(self, name, return_data):
		"""
			Called whenever an image has finished uploading.
			We need this becuase the progress callback does not return
			a final event when an item reaches 100%
				@name : the file that was uploaded
				@return_data: data to help construction of the images remote url
		"""
		widget_row = self.get_payload_item(filename = name)
		self.update_progress_widget( item_widget.progressbar, 100)
		widget_row['widget_remoteurl'].setText(return_data)

	def callback_payload_item_progress(self, name, current, total):
		"""
			Called whenever a portion of an image has been sent to the remote
			server.
				@name : the filename
				@current : current bytes sent so far
				@total : total amount of bytes to send.
		"""
#		widget_row = self.get_payload_item(filename = name)
#		if widget_row :
#			widget_progress = widget_row['widget_progress']
#			step= int( float(current)/float(total)*100 )
#			self.update_progress_widget(widget_progress, step)
#			self.parent.logger.info("Updating Widget %s [%s/%s](%s)" % (widget_progress, current, total, step ))

	def update_progress_widget(self, widget, value):
		"""
			Updates the progress bar (@widget), to @value
				@widget : the progress bar widget to update
				@value : the value to set between 0 and 100
		"""
		if value > 100 :
			value = 100
		widget.step = value
		widget.setValue( value )



#####################
##
##  Configuration Interface
##
class ConfigWindow(QtGui.QWidget):
	"""
		Provides an interface to create and edit new
		remote host profiles.
	"""
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



################################################################################
def main():
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = ImageUploader(sys.argv)
	app.mainWindow.show()
	sys.exit(app.exec_())

