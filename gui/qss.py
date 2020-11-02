from PySide2.QtGui import QBrush, QColor, QPalette, Qt


Stylesheet = """
    QWidget {
        color: #ddd;
        background: #333;
    }
    QWidget:disabled {
        color: #555;
        background-color: #252525;
    }
    QDialog {
        background-color: #252525;
    }
    QLabel{
        background: transparent;
    }
    QPlainTextEdit, QLineEdit:hover, QLineEdit:focus {
        border-style: solid;
        border: 2px solid #f7931e;
        border-radius: 4;
        selection-background-color: #f7931e;
    }

    QCheckBox::indicator:checked:hover, QCheckBox::indicator:unchecked:hover {
        border: 2px solid #f7931e;
    }
    QCheckBox::indicator:checked {
        background: #ddd;
        border: 2px solid #252525;
        border-radius: 6px;
    }
    QCheckBox::indicator:unchecked {
        background: #252525;
        border: 2px solid #252525;
        border-radius: 6px;
    }
    QScrollBar:vertical {
        background: transparent;
        width: 8px;
        border: 1px solid #252525;
    }
    QScrollBar::handle:vertical {
        background: #555;
        min-height: 20px;
        border-radius: 2px;
    }

    QScrollBar::handle:vertical:hover {
        background: #f7931e;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    QScrollBar:horizontal {
        background: transparent;
        height: 8px;
        border: 1px solid #252525;
    }
    QScrollBar::handle:horizontal {
        background: #555;
        min-width: 20px;
        border-radius: 2px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #f7931e;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }
    QSlider {
        min-height: 20px;
    }
    QSlider::groove:horizontal {
        border: None;
        height: 5px; 
        background: #252525;
        border-radius: 2px;
    }
    QSlider::handle:horizontal {
        background: #555;
        width: 16px;
        padding: -2px;
        margin: -6px 0;
        border: 2px solid #252525;
        border-radius: 8px;
    }
    QSlider::handle:horizontal:hover {
        border: 2px solid #f7931e;
    }
    QSlider::add-page:qlineargradient {
        background: 252525;
    }
    QSlider::sub-page:qlineargradient {
        background: #f7931e;
        border: 2px solid #252525;
        border-radius: 2px;
    }
    QPushButton {
        background-color: #555;
        border-width: 2;
        border-color: #555;
        border-style: solid;
        border-radius: 6;
        padding: 3px;
        padding-left: 5px;
        padding-right: 5px;
    }
    QPushButton:hover{
        border-width: 2px;
        border-color: #f7931e;
    }
    QPushButton:pressed {
        background-color: #f7931e;
    }

    QProgressBar{text-align: center; background-color: transparent}
    QProgressBar::chunk{background-color: #555;border:None;}

    QTabWidget::pane {border-top: 1px solid #252525; bottom:2px;}
    QTabWidget::tab-bar {left: 28px;}
    QTabWidget::tab-bar:top {top: 1px;}
    QTabWidget::tab-bar:bottom {bottom: 1px;}
    QTabWidget::tab-bar:left {right: 1px;}
    QTabWidget::tab-bar:right {left: 1px;}
    QTabBar{background:transparent;}
    QTabBar::tab {background:#333; font-weight: bold; width:55px}
    QTabBar::tab:!selected {background: #252525; color: #999}
    QTabBar::tab:!selected:hover {color: #BBB; border-top: 2px solid #f7931e}
    QTabBar::tab:top:!selected {margin-top: 3px;}
    QTabBar::tab:bottom:!selected {margin-bottom: 3px;}
    QTabBar::tab:left:!selected {margin-right: 3px;}
    QTabBar::tab:right:!selected {margin-left: 3px;}
    QTabBar::tab:top:selected {border-bottom-color: none;}
    QTabBar::tab:bottom:selected {border-top-color: none;}
    QTabBar::tab:left:selected {border-left-color: none;}
    QTabBar::tab:right:selected {border-right-color: none;}
    QTabBar::tab:top, QTabBar::tab:bottom {min-width: 8ex;margin-right: -1px;padding: 5px 10px 5px 10px;}
    QTabBar::tab:top:last, QTabBar::tab:bottom:last,QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {margin-right: 0;}
    QTabBar::tab:left:last, QTabBar::tab:right:last,QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {margin-bottom: 0;}
    QTabBar::tab:left, QTabBar::tab:right {min-height: 8ex;margin-bottom: -1px;padding: 10px 5px 10px 5px;}

    QTableWidget {
        border: 1px solid #282828;
        selection-background-color: #f7931e; 
        selection-color: #FFF; 
        background-color:#333333; 
        alternate-background-color: #292929;
    }
    QTableWidget::item { 
        margin: 0 5px 0 5px 
    }

    QHeaderView::section {
        Background-color:#282828;
        padding:5px;
        border:1px solid #333;
        font-weight: bold;
    }
"""

def getColor(r,g,b):
    brush = QBrush(QColor(r, g, b))
    brush.setStyle(Qt.SolidPattern)
    return brush

def getNukePalette():
    palette = QPalette()
    palette.setBrush(QPalette.Window, getColor(50, 50, 50))
    palette.setBrush(QPalette.WindowText, getColor(255, 255, 255))
    palette.setBrush(QPalette.Base, getColor(100, 100, 100))
    palette.setBrush(QPalette.AlternateBase, getColor(25, 25, 25))
    palette.setBrush(QPalette.ToolTipBase, getColor(255, 255, 220))
    palette.setBrush(QPalette.ToolTipText, getColor(0, 0, 0))
    palette.setBrush(QPalette.Text, getColor(245, 245, 245))
    palette.setBrush(QPalette.BrightText, getColor(255, 255, 255))
    palette.setBrush(QPalette.Button, getColor(80, 80, 80))
    palette.setBrush(QPalette.ButtonText, getColor(255, 255, 255))
    palette.setBrush(QPalette.Light, getColor(75, 75, 75))
    palette.setBrush(QPalette.Midlight, getColor(62, 62, 62))
    palette.setBrush(QPalette.Dark, getColor(25, 25, 25))
    palette.setBrush(QPalette.Mid, getColor(33, 33, 33))
    palette.setBrush(QPalette.Shadow, getColor(0, 0, 0))
    palette.setBrush(QPalette.Highlight, getColor(247, 147, 30))
    
    return palette