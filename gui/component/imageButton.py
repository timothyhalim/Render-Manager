from PySide2.QtGui import QPixmap
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QLabel


class ImageButton(QLabel):
	clicked = Signal()
	def __init__(self, imagepath, tooltip="", size=24):
		super(ImageButton, self).__init__()
		self.size = size
		
		self.setToolTip(f"<font color=#FFFFFF>{tooltip}</font>")
		self.setPixmap(QPixmap(imagepath).scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		self.setMaximumWidth(self.size)
		self.setMinimumWidth(self.size)
		self.setStyleSheet("background-color: rgb(40, 40, 40)")
	
	def enterEvent(self, event):
		self.setStyleSheet("background-color: rgb(40, 40, 40)")
	
	def leaveEvent(self, event):
		self.setStyleSheet("background-color: rgb(40, 40, 40)")
	
	def mousePressEvent(self, event):
		self.setStyleSheet("background-color: rgb(70, 70, 70)")
	
	def mouseReleaseEvent(self, event):
		self.clicked.emit()
		self.setStyleSheet("background-color: rgb(40, 40, 40)")