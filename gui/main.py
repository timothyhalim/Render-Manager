from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QTableWidgetItem

from .component.ProgressBar import CustomProgressBar
from . import Base

class UserInterface(Base.UserInterface):
    def __init__(self):
        super().__init__()

    def connect_signal(self, db):
        self.db = db
        # Signals
        self.job_action_start_button.clicked.connect(self.start_render)
        self.job_action_stop_button.clicked.connect(self.stop_render)
        
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

        self.job_list_table.itemSelectionChanged.connect(self.row_selected)

    def start_render(self):
        self.db.update_host(enabled=True)

    def stop_render(self):
        self.db.update_host(enabled=False)

    def addCell(self, row, col, content, alignment = [], tooltip = None):
        cell = QTableWidgetItem()
        cell.setText(str(content))
        cell.setData(Qt.UserRole, content)
        self.job_list_table.setItem(row, col, cell)
        for a in alignment:
            cell.setTextAlignment(a)
        if tooltip:
            cell.setToolTip(tooltip)
        return (cell)

    def build_job_list(self, jobs):
        self.job_list_table.setRowCount(len(jobs))
        for job in jobs:
            row = job.id-1
            job_code = self.addCell(row, 0, job.code, alignment = [Qt.AlignVCenter | Qt.AlignRight])
            submit_date = self.addCell(row, 1, job.submit_date.strftime("%Y-%m-%d %H:%M:%S"), alignment = [Qt.AlignVCenter | Qt.AlignLeft])
            submitter = self.addCell(row, 2, job.submitter.name, alignment = [Qt.AlignVCenter | Qt.AlignLeft])
            file_path = self.addCell(row, 3, job.file_path, 
                                        alignment = [Qt.AlignVCenter | Qt.AlignLeft], tooltip = job.file_path)
            layer = self.addCell(row, 4, job.layer, alignment = [Qt.AlignVCenter | Qt.AlignLeft])
            weight = self.addCell(row, 5, job.weight, alignment = [Qt.AlignCenter])
            progressBar = CustomProgressBar(job)
            self.job_list_table.setCellWidget(row, 6, progressBar)
            eta = self.addCell(row, 7, str(job.eta()), alignment = [Qt.AlignCenter])
            workers = self.addCell(row, 8, len(job.clients()), alignment = [Qt.AlignCenter])
            # actionCell = ActionCell(row)
            # self.job_list_table.setCellWidget(row, 6, actionCell)
            
    def get_selected_row(self):
        items = self.job_list_table.selectedIndexes()
        rows = []
        for item in items:
            row = item.row()
            if not row in rows:
                rows.append(row)
        return rows
    
    def row_selected(self):
        selected_rows = self.get_selected_row()
        if selected_rows:
            if len(selected_rows) > 1:
                print ("Multiple selected")
            else:
                print ("One selected")
                id = self.job_list_table.item(selected_rows[0], 0).text()
                print(id)
                # for job in self.jobList:
                #     if job.id == id:
                #         self.jobPriorityControl.setValue(job.priority)
                #         self.jobWorkerControl.setValue(job.workerCount)