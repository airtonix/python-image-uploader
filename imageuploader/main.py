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
from .widgets import PayloadItemProgressBar, IconListView, IconDisplayItem


__author__ = "Zenobius Jiricek"
__author_email__ = "airtonix@gmail.com"
__author_website__ = "airtonix.net"
__application_name__ = "pyImagePoster"
__application_version__ = "0.0.2dev"

application_path = os.path.abspath( os.path.dirname(__file__) )
configuration_path = utils.assure_path( os.path.join( os.getenv("HOME"), '.config', __application_name__) )
log_path = utils.assure_path( os.path.join( os.getenv("HOME"), '.local','share', __application_name__,'logs') )

log_file = logging.FileHandler( os.path.join(log_path,"debug.log") )
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file.setFormatter(log_formatter)

logger = logging.getLogger(__application_name__)
logger.addHandler(log_file)
logger.setLevel(logging.INFO)

logger.info( "application_path = %s" % application_path)

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
		self.mainWindow.resize(270, 540)

		self.mainWindow.statusBar().showMessage("Ready")

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None, *args):
		super(MainWindow, self).__init__(*args)
		self.parent = parent

		self.centralWidget = QtGui.QWidget()
		self.setCentralWidget(self.centralWidget)

		self.create_header()
		self.create_payload_preview()
		main_layout = QtGui.QGridLayout()
		main_layout.addWidget( self.header_row, 0,0, QtCore.Qt.AlignTop)
		main_layout.addWidget( self.payload_preview_row,1,0, QtCore.Qt.AlignTop)

		self.centralWidget.setLayout(main_layout)

		self.populate_payload_items()
		self.setFocus()

	##################
	## Top Level Application GUI Action Methods

	def exit(self):
		"""
			Stop any operations, and quit the application.
			TODO: implement this.
		"""
		pass

	##################
	## Top Level Application GUI Creation Methods
	def create_header(self):
		self.header_row = QtGui.QWidget()

		layout = QtGui.QHBoxLayout()

		pixmap_header_logo = QtGui.QPixmap( os.path.join(self.parent.application_path, "resources", "icons", "application_logo.png" ) )
		label_header_logo = QtGui.QLabel(self)
		label_header_logo.setPixmap( pixmap_header_logo )
		layout.addWidget( label_header_logo )

		self.label_application_title = QtGui.QLabel()
		self.label_application_title.setText( str( self.parent.application_title ) )
		layout.addWidget( self.label_application_title , QtCore.Qt.AlignLeft)

		self.combo_host_chooser = QtGui.QComboBox(self)
		self.populate_host_chooser(self.combo_host_chooser, self.parent.upload_manager.profiles )
		self.connect(self.combo_host_chooser, QtCore.SIGNAL('activated(QString)'), self.combo_host_chooser_activated)
		layout.addWidget( self.combo_host_chooser)

		pixmap_config_icon = QtGui.QIcon( os.path.join(self.parent.application_path, "resources", "icons", "config.png" ) )
		button_config = QtGui.QPushButton()
		button_config.setFlat(True)
		button_config.setFixedSize(32,32)
		button_config.setIcon(pixmap_config_icon )

		self.connect(button_config, QtCore.SIGNAL('clicked()'), self.button_config_clicked )

		layout.addWidget(button_config, stretch = 0)

		self.header_row.setLayout(layout)

	def create_payload_preview(self):
		"""
			Creates the main interaction area, where each payload item (an Pixmap)
			is displayed.
		"""
		self.payload_preview_row = QtGui.QWidget()
		layout = QtGui.QHBoxLayout()

		self.payload_view = QtGui.QListWidget() #IconListView( self.payload_preview_row )
		self.payload_view.setMovement(QtGui.QListView.Static)  #otherwise the icons are draggable
		self.payload_view.setResizeMode(QtGui.QListView.Adjust) #Redo layout every time we resize
		self.payload_view.setViewMode(QtGui.QListView.IconMode) #Layout left-to-right, not top-to-bottom

		layout.addWidget( self.payload_view )
		self.payload_preview_row.setLayout(layout)

	def populate_host_chooser(self, widget, profiles):
		for hostname, data in profiles.items() :
			widget.addItem( hostname.split(".")[0] )

	def populate_payload_items(self):

		for item in self.parent.upload_manager.files:
			listItem = QtGui.QListWidgetItem()
			listItem.setText( os.path.splitext(item)[0] )
			listItem.setIcon( QtGui.QIcon( QtGui.QPixmap(item) ) )
			listItem.setSizeHint(QtCore.QSize(100,100))
			#payload_item = IconDisplayItem( item,  )
			self.payload_view.addItem( listItem )

		self.payload_view.setAutoFillBackground(True)


	def create_payload_item(self, filename):
		pixmap_item = QtGui.Pixmap(filename)
		icon_item = IconDisplayItem( filename , pixmap_item )
		return icon_item

	##################
	## Interface Callback Methods
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
		pass

	def button_config_clicked(self):
		"""
			config button used to access the configuration interface
		"""
		self.config_interface = ConfigWindow(self)
		self.config_interface.show()

	def button_ok_clicked(self):
		"""
			start/deliver/begin button.
			Begins the delivery of payload items to designated remote host
		"""
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
		"""
			Stops any delivery process operations
		"""
		self.close()



def main():
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = ImageUploader(sys.argv)
	app.mainWindow.show()
	sys.exit(app.exec_())

