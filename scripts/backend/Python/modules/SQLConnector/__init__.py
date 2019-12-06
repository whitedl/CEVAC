#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import pyodbc

class SQLConnector():
    """ Collection of helper methods to query the MS SQL Server database.
    """

    def __init__(self, port=1433):
        self.PORT = str(port)
        self.DRIVER = '{ODBC Driver 17 for SQL Server}'
        self.SERVER = '130.127.218.11'
        self.DATABASE = 'WFIC-CEVAC'
        self.UID = 'wficcm'
        self.PWD = '5wattcevacmaint$'
        conn_str = (
                'DRIVER=' + self.DRIVER + ';' +
                'SERVER=' + self.SERVER + ';' +
                'PORT=' + self.PORT + ';' +
                'DATABASE=' + self.DATABASE + ';'
                'UID=' + self.UID + ';'
                'PWD=' + self.PWD
                )

        self._connection = pyodbc.connect(conn_str)        
        pyodbc.pooling = False

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

    def __repr__(self):
        return f"MS-SQLServer('{self.username}', <password hidden>, '{self.host}', '{self.port}', '{self.db}')"

    def __str__(self):
        return f"MS-SQLServer Module for STP on {self.host}"

    def __del__(self):
        self._connection.close()

    ## imported methods
    from ._cursor import cursor
    from ._exec_sql import exec_sql

