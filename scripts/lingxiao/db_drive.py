# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:32:45 2019

@author: Lingxiao
"""

import pymssql



class db_obj:
    def __init__(self):
        self.account = {'server': '130.127.218.11',
                       'user': 'wficcm',
                       'password': '5wattcevacmaint$',
                       'database': 'WFIC-CEVAC'}
        self.dbconnect = pymssql.connnect(**self.account)
        self.db_cursor = self.dbconnect.cursor()
        self.args=''
        
    def get_data(self,sql_command):
        self.args = sql_command
        self.db_cursor.execute(self.args)
        res = self.db_cursor.fetchall()
        self.db_cursor.close()
        self.dbconnect.close()
        return res
        
        





#if __name__ == '__main__':
    
    
    