import sys
from random import randint

from PySide2.QtGui import QColor, QPixmap, Qt

from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QStackedLayout, QVBoxLayout, QWidget

class Chunk(QWidget):
    def __init__(self, text=""):
        super().__init__()
        self.setAutoFillBackground(True)
        self.update_color(rgb=(randint(0,255),randint(0,255),randint(0,255)))
        self.setToolTip(str(text))

    def update_color(self, rgb):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(rgb[0], rgb[1], rgb[2]))
        self.setPalette(p)

class ChunkBar(QWidget):
    def __init__(self, parent = None, chunks=200):
        super().__init__(parent)
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.setMargin(0)
        self.frame_layout.setSpacing(0)
        self.chunks = [Chunk(x) for x in range(chunks)]
        for chunk in self.chunks:
            self.frame_layout.addWidget(chunk)

class CustomProgressBar(QWidget):
    def __init__(self, size=18):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.layout.setMargin(0)

        self.statusIcon = QLabel("Ico")
        self.statusIcon.setMaximumWidth(size)
        self.statusIcon.setMinimumWidth(size)

        self.statusLabel = QLabel("100.99%")
        self.statusLabel.setMaximumWidth(50)
        self.statusLabel.setMinimumWidth(50)
        
        self.bar = ChunkBar(chunks=100)

        self.layout.addWidget(self.statusIcon)
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.bar)
        
        self.show()
        
    
if __name__ == '__main__':
    # try:
    app = QApplication(sys.argv)
    w = CustomProgressBar()
    app.exec_()
        