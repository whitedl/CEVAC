import pyodbc
import sys
import re
import numpy as np
import pandas as pd

class new_bsql:
    def __init__(self):
        self.DRIVER = "ODBC Driver 17 for SQL Server"
        self.SERVER = "130.127.218.11"
        self.DATABASE = "WFIC-CEVAC"
        self.USERNAME = "wficcm"
        self.PASSWORD = "5wattcevacmaint$"
        self.CHARSET = "utf-8"
        #self.command = sql_command
    
    def __getConnect(self):
        '''
        link the SQL Server with stored config
        '''
        try:
            self.conn = pyodbc.connect(DRIVER=self.DRIVER,
                                       SERVER=self.SERVER,
                                       DATABASE=self.DATABASE,
                                       UID=self.USERNAME,
                                       PWD=self.PASSWORD,
                                       charset=self.CHARSET)
            cur = self.conn.cursor()
        except Exception as ex:
            print("SQL Server connecting error,reason is: ", ex)
            sys.exit()
        return cur

    def RequestData(self, command):
        cur = self.__getConnect()
        try:
            cur.execute(command)
            rows = cur.fetchall()
            '''
            columns = [column [0] for cur.description]
            print(columns)
            '''
        except pyodbc.Error as ex:
            frame = list(sys._current_frames().values())[0]
            error_source = frame.f_back.f_globals['__file__'] #Error source
            temp_ex = str(ex).replace("'","''") #Error message
            error_table = self.find_table(command)
            self.ExecQuery(f"INSERT INTO CEVAC_ERRORS (TableName, ErrorMessage, UTCDateTime, ProcessName) \
                VALUES ('{error_table}', '{temp_ex}', GETDATE(), '{str(error_source)}');")
            print("SQL Server.Error in RequestData: ", ex)
            sys.exit()
        cur.close()
        self.conn.close()
        return rows
    
    def RequestDataframe(self, command):
        cur = self.__getConnect()
        df = pd.read_sql(command,self.conn)
        cur.close()
        self.conn.close()
        return df

    def InsertDataframe(self, df, tablename, method="replace"):
        cur = self.__getConnect()
        df.to_sql(con=self.conn, name=tablename, if_exists=method, index=False)
        cur.close()
        self.conn.close()
        return 1


    def ExecQuery(self, command):
        cur = self.__getConnect()
        try:
            cur.execute(command)
            self.conn.commit()
        except pyodbc.Error as ex:
            frame = list(sys._current_frames().values())[0]
            error_source = frame.f_back.f_globals['__file__']
            temp_ex = str(ex).replace("'","''")
            error_table = self.find_table(command)
            self.ExecQuery(f"INSERT INTO CEVAC_ERRORS (TableName, ErrorMessage, UTCDateTime, ProcessName) \
                VALUES ('{error_table}', '{temp_ex}', GETDATE(), '{str(error_source)}');")
            print("SQL Server.Error in ExecQuery: ", ex)
        cur.close()
        self.conn.close()
        return 1
    
    def RequestData_csv(self, command, filepath="./temp_csv.csv"):
        df = self.RequestDataframe(command)
        df.to_csv(filepath,index=None)
        return 1
    

    def find_table(self,command):
        pattern = re.compile(r"CEVAC\S+")
        match = pattern.findall(command)
        if match:
            return (" & ".join(match))
        else:
            return("NULL")

if __name__ == "__main__":
    test_query = "select * from test;"
    test_data = new_bsql().RequestData(test_query)
    print(test_data)