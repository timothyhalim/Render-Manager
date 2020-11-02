import os
import sys

from PySide2.QtGui     import QPixmap, QIcon
from PySide2.QtCore    import Qt, QRect
from PySide2.QtWidgets import QDialog, QWidget, QLabel, QFrame, \
                              QVBoxLayout, QHBoxLayout, \
                              QCheckBox, QTabWidget, \
                              QTableWidget, QTableWidgetItem, \
                              QAbstractItemView \

from .QSS import Stylesheet, getNukePalette
from .component import *
    
def resourcePath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.join(os.path.dirname(__file__),"icons")
    
    return os.path.join(base_path, relative_path)
    
class UserInterface(QDialog):
    def __init__(self, parent=None):
        super(UserInterface, self).__init__(parent)
        self.setWindowTitle("Render Manager by Timo.ink")
        self.setWindowIcon(QIcon(resourcePath("Timo.png")))
        self.setWindowFlags( self.windowFlags() |
                             Qt.WindowSystemMenuHint |
                             Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_DeleteOnClose, Qt.WA_TranslucentBackground)
        self.setStyleSheet(Stylesheet)
        self.setPalette(getNukePalette())
        self.resize(1600, 350)
        
        self.logo = QLabel() 
        self.logo.setPixmap(QPixmap(resourcePath("Timo.png")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setMinimumSize(20, 20)
        self.logo.setGeometry(QRect(4, 4, 20, 20))
        self.logo.setParent(self)
        
        self.setup_ui()
        self.show()
        
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_tab_widget = QTabWidget()
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.setup_job_ui()
        self.setup_settings_ui()
        
    def setup_job_ui(self):
        self.job_tab = QWidget()
        self.job_master_layout = QVBoxLayout(self.job_tab)
        self.job_master_layout.setContentsMargins(0,0,0,0)
        self.job_master_layout.addSpacing(5)
        self.main_tab_widget.addTab(self.job_tab, "Job")
        
        self.setup_job_ui_action_bar()
        self.setup_job_ui_list()
        
    def setup_job_ui_action_bar(self):
        # Button bar
        self.job_action_layout = QHBoxLayout()
        self.job_action_layout.setContentsMargins(5,0,5,0)
        
        # Divider
        self.job_action_div_one = QFrame()
        self.job_action_div_two = QFrame()
        self.job_action_div_three = QFrame()
        for d in [self.job_action_div_one, self.job_action_div_two, self.job_action_div_three]:
            d.setFrameShape(QFrame.VLine)
            d.setFrameShadow(QFrame.Sunken)
        
        # Add Buttons
        self.job_action_start_button = ImageButton(resourcePath("Start.png"), "Start Queue", 24)
        self.job_action_stop_button = ImageButton(resourcePath("Stop.png"), "Stop Queue", 24)
        for button in (self.job_action_start_button, 
                       self.job_action_stop_button, 
                       self.job_action_div_one):
            self.job_action_layout.addWidget(button)
        
        # Add Filter
        self.job_action_filter_waiting = QCheckBox("Waiting")
        self.job_action_filter_running = QCheckBox("Running")
        self.job_action_filter_disabled = QCheckBox("Disabled")
        self.job_action_filter_finished = QCheckBox("Finished")
        self.job_action_filter_search = SearchBar(placeholder="Search")
        
        for button in (self.job_action_filter_waiting, 
                       self.job_action_filter_running, 
                       self.job_action_filter_disabled, 
                       self.job_action_filter_finished):
            button.setChecked(True)
            self.job_action_layout.addWidget(button)
        self.job_action_layout.addWidget(self.job_action_filter_search)
        
        self.job_action_layout.addWidget(self.job_action_div_two)
        
        # Add Buttons
        self.job_action_enable_button = ImageButton(resourcePath("Enable.png"), "Enable selected Jobs", 24)
        self.job_action_disable_button = ImageButton(resourcePath("Disable.png"), "Disable selected Jobs", 24)
        self.job_action_check_button = ImageButton(resourcePath("Check.png"), "Check selected Jobs", 24)
        self.job_action_reset_button = ImageButton(resourcePath("Reset.png"), "Reset selected Jobs", 24)
        self.job_action_delete_button = ImageButton(resourcePath("Delete.png"), "Delete selected Jobs", 24)
        for button in (self.job_action_enable_button, 
                       self.job_action_disable_button, 
                       self.job_action_check_button, 
                       self.job_action_div_three, 
                       self.job_action_reset_button, 
                       self.job_action_delete_button):
            self.job_action_layout.addWidget(button)
        self.job_action_layout.addStretch()
        
        # Add to master layout
        self.job_master_layout.addLayout(self.job_action_layout)
        
        # Signals
        # self.stopButton.clicked.connect(self.stopRender)
        # self.startButton.clicked.connect(self.startRender)
        
        # for button in (self.job_action_filter_waiting, 
                       # self.job_action_filter_running, 
                       # self.job_action_filter_disabled, 
                       # self.job_action_filter_finished):
            # button.stateChanged.connect(self.filterTable)
            
        # self.job_action_enable_button.clicked.connect(self.enableJobs)
        # self.job_action_disable_button.clicked.connect(self.disableJobs)
        # self.job_action_check_button.clicked.connect(self.checkJobs)
        # self.job_action_reset_button.clicked.connect(self.resetJobs)
        # self.job_action_delete_button.clicked.connect(self.deleteJobs)
        
    def setup_job_ui_list(self):
        # Add Table 
        self.job_list_layout = QHBoxLayout()
        
        self.job_list_table = QTableWidget()
        self.job_list_table.setSortingEnabled(True)
        self.job_list_table.setAlternatingRowColors(True)
        self.job_list_table.setMinimumHeight(120)
        self.job_list_table.setColumnCount(10)
        self.job_list_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.job_list_table.horizontalHeader().setStretchLastSection(True)
        
        self.job_list_table.setRowCount(1)
        column_number = 0
        for name, column_width in (("ID", 50), ("Date", 150),  ("Submitter", 150), ("File", 550), ("Layer", 100), ("Weight", 80),  ("Progress", 200), ("ETA", 120),  ("Workers", 80), ("Action", 80)):
            self.job_list_table.setHorizontalHeaderItem(column_number, QTableWidgetItem(name))
            self.job_list_table.setColumnWidth(column_number, column_width)
            column_number += 1
        self.job_list_table.setColumnCount(column_number)
        self.job_list_table.setRowCount(0)
        
        self.job_list_table_vertical_header = self.job_list_table.verticalHeader()
        self.job_list_table_vertical_header.setDefaultSectionSize(35)
        self.job_list_table_vertical_header.setMinimumSectionSize(35)
        self.job_list_table.setShowGrid(False)
        
        self.job_list_layout.addWidget(self.job_list_table)
        
        
        # Add to master layout
        self.job_master_layout.addLayout(self.job_list_layout)
        
        # Signals
        # self.job_list_table.itemSelectionChanged.connect(self.rowSelected)
        
    def setup_settings_ui(self):
        self.settings_tab = QWidget()
        self.settings_master_layout = QVBoxLayout(self.settings_tab)
        self.settings_master_layout.setContentsMargins(0,0,0,0)
        self.settings_master_layout.addSpacing(5)
        self.main_tab_widget.addTab(self.settings_tab, "Settings")
        