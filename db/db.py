import traceback
import sys
import os
import sqlite3


class db():
    def __init__(self, dbpath):
        self.connect(dbpath)
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print ("Connection Closed!")
        
    def connect(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        
    def table_create(self, table_name="Table", keys={'id':['INTEGER', 'PRIMARY KEY'], 'created_at': 'DATETIME'}):
        if table_name:
            command = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            for i, (k, type) in enumerate(keys.items()):
                attributes = str(' ').join(type)
                command += f"{k} {attributes}"
                if i < len(keys.keys()) -1:
                    command += ",";
                command += "\n"
            command += f");"
            
            self.cursor.execute(command)
            self.connection.commit()
        
    def table_add_column(self, table_name=""):
        pass
        
    def insert_data(self, table_name="", values=[]):
        if table_name:
            if values:
                command = f"INSERT INTO {table_name} "
                command += "VALUES \n"
                command += str([tuple(v) for v in values])[1:-1].replace("'null'", "null").replace("'CURRENT_TIMESTAMP'", "CURRENT_TIMESTAMP")
                print(command)
                self.cursor.execute(command)
                self.connection.commit()
        
    def fetchAll(self, table_name="", selection=["*"], where="", sort_by="", sort="ASC", group_by="", all=True):
        if table_name:
            command = f"SELECT {selection} FROM {table_name}\n"
            if where:
                command += f"WHERE {where}\n"
            if sort_by:
                command += f"ORDER BY {sort_by} {sort}\n"
            if group_by:
                command += f"GROUP BY {group_by}\n"
            command += ";"
            
            self.cursor.execute(command)
            if all:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall()
                
                
if __name__ == '__main__':
    try:
        dbpath = os.path.join(os.path.abspath(__file__), "..", "..", "RenderManager.db")
        db = db(dbpath)
        
        def create_table():
            db.table_create('jobs', keys={
                'id': ['INTEGER', 'PRIMARY KEY', 'AUTOINCREMENT'],
                'date': ['DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'NOT NULL'],
                'code': ['TEXT', 'NOT NULL', 'UNIQUE'],
                'submitter': ['TEXT'],
                'file': ['TEXT', 'NOT NULL'],
                'layer': ['TEXT', 'NOT NULL'],
                'weight': ['INTEGER', 'DEFAULT 1'],
                'apps': ['TEXT'],
                'executor': ['TEXT'],
                'status': ['TEXT'],
                'info': ['TEXT'],
            })
        
        def submit_data():
            db.insert_data('jobs', values=[
                ["null", "CURRENT_TIMESTAMP", "XBAC", "timothy.halim", r"J:\UCG\Episodes\Scenes\EP100\SH002.00A\UCG_EP100_SH002.00A_CMP.nk", "WRITE_IMG", 0, r"J:\UCG\UCG_Nuke10.bat", "renderNuke.py", "Waiting", ""],
                ["null", "CURRENT_TIMESTAMP", "BZCR", "timothy.halim", r"J:\UCG\Episodes\Scenes\EP100\SH002.00A\UCG_EP100_SH002.00A_CMP.nk", "WRITE_IMG", 0, r"J:\UCG\UCG_Nuke10.bat", "renderNuke.py", "Waiting", ""]
            ])
        create_table()
        submit_data()
    except Exception as e: 
        print(traceback.format_exc())
input("Press Enter to continue...")