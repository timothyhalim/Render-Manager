from PySide2.QtGui import QColor, QPalette, Qt
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget

from random import randint

class Chunk(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.setAutoFillBackground(True)
        # self.update_color(rgb=(randint(0,255),randint(0,255),randint(0,255)))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setToolTip(f"{frame.number}<br>{frame.status.name}")
        self.color = [
            (128,128,128), # Idle
            (50,50,255), # Waiting
            (50,128,50), # Ready
            (50,255,50), # Running
            (255,50,50), # Error
            (50,50,50), # Disabled
            (255,255,255), # Finished
        ]
        self.update_color(self.color[frame.status.id-1])

    def update_color(self, rgb):
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})')

class ChunkBar(QWidget):
    def __init__(self, job, parent = None):
        super().__init__(parent)
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.setMargin(0)
        self.frame_layout.setSpacing(0)
        self.chunks = [Chunk(x) for x in job.frames()]
        for chunk in self.chunks:
            self.frame_layout.addWidget(chunk)

class CustomProgressBar(QWidget):
    def __init__(self, job, size=18 ):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.layout.setMargin(0)

        self.statusIcon = QLabel("Ico")
        self.statusIcon.setMaximumWidth(size)
        self.statusIcon.setMinimumWidth(size)

        self.statusLabel = QLabel("100.99%")
        self.statusLabel.setMaximumWidth(50)
        self.statusLabel.setMinimumWidth(50)
        
        self.bar = ChunkBar(job)

        self.layout.addWidget(self.statusIcon)
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.bar)
        