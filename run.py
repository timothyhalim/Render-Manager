import sys
import os
import traceback

from db import db
from gui import main


dbpath = os.path.join(os.path.abspath(__file__), "..", "RenderManager.db")

class RenderManager():
    def __init__(self, *args):
        super(RenderManager, self).__init__()
        
        self.app = main.QApplication()
        self.app.setStyle("Fusion")
        self.wind = main.UserInterface()
        
        # self.db = db.db(dbpath)
        # self.init_db()

    def init_db(self):
        self.db.table_create('jobs', keys={
            'id': ['INTEGER', 'PRIMARY KEY'],
            'code': ['TEXT'],
            'submitter': ['TEXT'],
            'file': ['TEXT'],
            'layer': ['TEXT'],
            'weight': ['INTEGER'],
            'info': ['TEXT'],
        })
        
    def submit_job(self):
        pass
        
    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    # try:
    app = RenderManager(sys.argv)
    app.run()
        
    # except Exception as e: 
    #     print(traceback.format_exc())
    #     input("Press Enter to continue...")