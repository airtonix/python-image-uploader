from PySide import QtCore,QtGui

class PayloadItemProgressBar(QtGui.QProgressBar):
	def __init__(self, *args, **kwargs):
		super(PayloadItemProgressBar, self).__init__(*args, **kwargs)
		self.timer = QtCore.QBasicTimer()
		self.step = 0

	def set_step(self, value):
		self.step = value
		self.setValue(value)

	def timerEvent(self, event):
		if self.step >= 100:
			self.timer.stop()
			return
#		self.step = self.step + 1
		self.setValue(self.step)


class IconListView(QtGui.QListView):
	def __init__(self, parent=None):
		super(IconListView, self).__init__(parent)
		self.setFlow(QtGui.QListView.TopToBottom)
		self.setLayoutMode(QtGui.QListView.SinglePass)
		self.setResizeMode(QtGui.QListView.Adjust)
		self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.setSelectionRectVisible(True)
		self.setSpacing(1)
		self.setViewMode(QtGui.QListView.IconMode)
		self.setWrapping(True)


class IconDisplayItem(QtGui.QWidget):
	def __init__(self, title=None, pixmap_uri=None, progress=None):
		QtGui.QWidget.__init__(self)
		self.size=100
		self.resize(self.size,self.size)
		self.setMinimumSize(self.size,self.size)
		self.text = title
		self.pixmap_uri = pixmap_uri

		self.progressbar = PayloadItemProgressBar(self)
		self.progressbar.setRange(0, 100)
		self.progressbar.setValue(0)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.progressbar)

		self.setLayout(layout)

	def setText(self, text):
		self.text = text

	def setIcon(self, pixmap):
		self.pixmap = pixmap

	def setProgress(self, value):
		self.progressbar.set_step(value)

	def paintEvent(self,event):
#		pixmap = QtGui.QPixmap( self.pixmap_uri )
		painter = QtGui.QPainter(self)
		painter.drawText(self.size//2,self.size//2,str(self.text))

#####################
##
##  Payload Item List View
##   subclassed QWidgetList

class PayloadListWidget(QtGui.QListWidget):
	def __init__(self,*args, **kwargs):
		super(PayloadListWidget, self).__init__()


	def items(self):
		for index in range(self.count()):
			yield self.item(index)

