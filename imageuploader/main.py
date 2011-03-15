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
from .widgets import PayloadItemWidget, PayloadListWidget, ApplicationHeader
from .tags import TagManager

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
logger.info("%s%s%s" % ("="*32, "[ Begin New Application Session ]", "="*32))
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
		self.resource_path = os.path.join(self.application_path, "resources")

		self.application_title = __application_name__
		self.configuration_path = configuration_path
		self.stylesheets = [ os.path.join(self.resource_path,"styles",filename) for filename in os.listdir( os.path.join( self.resource_path, "styles") )]



		self.logger = logger
		self.tag_manager = TagManager(self)

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
	"""
		Main Application Window
			Themeing Notes
			--------------
			  + look for the setObjectName(string_name), they let you know what
			  objects can be styled by id css syntax
	"""

	def __init__(self, parent=None, *args):
		super(MainWindow, self).__init__(*args)
		self.parent = parent

		self.current_style = open( self.parent.stylesheets[0] )
		self.centralWidget = QtGui.QFrame()
		self.centralWidget.setObjectName('canvas')
		self.centralWidget.setStyleSheet( self.current_style.read() )
		self.setCentralWidget(self.centralWidget)

		application_logo_path = os.path.join(self.parent.resource_path, "icons", "application_logo.png" )
		self.parent.logger.info("Creating ApplicationHeader with : logo:%s, title:%s" % (application_logo_path, __application_name__) )

		self.header_row = ApplicationHeader(
			application_logo_path = application_logo_path,
			application_title = __application_name__
		)
		self.payload_list = PayloadListWidget(self)
		self.footer_row = self.create_footer()


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

	def create_footer(self):
		"""
			Interface Construction :
				Build the Footer Area.
		"""
		row = QtGui.QWidget()
		row.setObjectName('footer')
		layout = QtGui.QHBoxLayout()
		layout.setObjectName('footer-inner')
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
		button_config.setObjectName('configuration-button')
		self.connect(button_config, QtCore.SIGNAL('clicked()'), self.button_config_clicked )
		layout.addWidget(button_config, stretch = 0)

		# button to start the upload process
		pixmap_start_delivery_icon = QtGui.QIcon( os.path.join(self.parent.application_path, "resources", "icons", "start_delivery.png" ) )

		button_start_delivery = QtGui.QPushButton()
		button_start_delivery.setObjectName('deliver-payload-button')
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
#		for item in self.payload_list.items():
#			if item.progressbar.timer.isActive():
#				self.parent.logger.info("Stopping Widget %s.timer" % item.progressbar)
#				item.progressbar.timer.stop()
#			else:
#				self.parent.logger.info("Starting Widget %s.timer" % item.progressbar)
#				item.progressbar.startTimer()

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
		self.parent.logger.info("callback_payload_item_beforestart : %s." % name)
		payload_item = self.payload_list.get_item(filename = name)
		payload_item.set_progress(0)

	def callback_payload_item_completed(self, name, return_data):
		"""
			Called whenever an image has finished uploading.
			We need this becuase the progress callback does not return
			a final event when an item reaches 100%
				@name : the file that was uploaded
				@return_data: data to help construction of the images remote url
		"""
		self.parent.logger.info("callback_payload_item_completed : %s : %s" % (name, return_data))
		payload_item = self.payload_list.get_item(filename = name)
		payload_item.set_label_url( "%s" % return_data )

		if payload_item :
			self.parent.logger.info(">> : %s " %  payload_item.get_label_url() )
			payload_item.set_label_url( return_data )
		else :
			print "Could not find item"

	def callback_payload_item_progress(self, *args):
		"""
			Called whenever a portion of an image has been sent to the remote
			server.
				@name : the filename
				@current : current bytes sent so far
				@total : total amount of bytes to send.
		"""
		form_object, current, total = args
		if hasattr(form_object, "filename") :
			payload_item = self.payload_list.get_item(filename = form_object.filename)
			if payload_item :
				step= int( float(current)/float(total)*100 )
				payload_item.set_progress( current )
				self.parent.logger.info("callback_payload_item_progress : > %s [ %s ] [%s/%s]" % (form_object.filename, step, current, total ))

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

