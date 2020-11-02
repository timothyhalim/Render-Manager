import sys
import os
import traceback

from db import Controller
from gui import Main

class RenderManager():
    def __init__(self, *args):
        super(RenderManager, self).__init__()
        
        self.app = Main.QApplication()
        self.app.setStyle("Fusion")
        self.wind = Main.UserInterface()
        
        dbpath = os.path.join(os.path.abspath(__file__), "..", "RenderManager.db")
        self.db = Controller.init(dbpath)

        self.build_list()
        
    def build_list(self):
        jobs = Controller.get_all_job()
        self.wind.build_job_list(jobs)

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