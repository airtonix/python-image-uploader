from PySide import QtCore,QtGui

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
	def __init__(self, title, pixmap_uri):
		QtGui.QWidget.__init__(self)
		self.size=100
		self.resize(self.size,self.size)
		self.setMinimumSize(self.size,self.size)
		self.text = title
		self.pixmap_uri = pixmap_uri

	def paintEvent(self,event):
		pixmap = QtGui.QPixmap( self.pixmap_uri )
		painter = QtGui.QPainter(self)
		painter.drawText(self.size//2,self.size//2,str(self.text))

