from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QTableWidgetItem

from .component.ProgressBar import CustomProgressBar
from . import Base

class UserInterface(Base.UserInterface):
    def __init__(self):
        super().__init__()

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
            job_code = self.addCell(row, 0, job.code, alignment = [Qt.AlignLeft,Qt.AlignVCenter])
            submit_date = self.addCell(row, 1, job.submit_date.strftime("%y%m%d %H:%M:%S"), alignment = [Qt.AlignLeft,Qt.AlignVCenter])
            submitter = self.addCell(row, 2, job.submitter.name, alignment = [Qt.AlignLeft,Qt.AlignVCenter])
            file_path = self.addCell(row, 3, job.file_path, 
                                        alignment = [Qt.AlignLeft,Qt.AlignVCenter], tooltip = job.file_path)
            layer = self.addCell(row, 4, job.layer, alignment = [Qt.AlignLeft,Qt.AlignVCenter])
            weight = self.addCell(row, 5, job.weight, alignment = [Qt.AlignCenter])
            progressBar = CustomProgressBar(job)
            self.job_list_table.setCellWidget(row, 6, progressBar)
            eta = self.addCell(row, 7, str(job.eta()), alignment = [Qt.AlignCenter])
            workers = self.addCell(row, 8, len(job.clients()), alignment = [Qt.AlignCenter])
            # actionCell = ActionCell(row)
            # self.job_list_table.setCellWidget(row, 6, actionCell)
            