#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import pyodbc
import sqlalchemy
import cx_Oracle
import urllib.parse

class SQLConnector():
    """ Collection of helper methods to query the MS SQL Server database.
    """
    ## imported methods
    from ._cursor import cursor
    from ._exec_sql import exec_sql
    from ._exec_sql import to_sql
    from ._exec_sql import sql_value
    from ._exec_sql import exec_only

    def __init__(self, flavor='mssql', port=1433):
        self.engine = None
        self.flavor = flavor
        if self.flavor == 'mssql':
            self.init_ms('wficcm','5wattcevacmaint$')
            self.flavor = 'mssql'
        elif flavor == 'oracle':
            self.init_oracle('CEVAC','fmocevac2019')
            self.flavor = 'oracle'
        else:
            print('incorrect flavor')

    def init_ms(self, UID, PWD, PORT=1433, SERVER='130.127.218.11', DATABASE='WFIC-CEVAC', DRIVER='ODBC Driver 17 for SQL Server'):
        self.PORT = PORT
        self.DRIVER = DRIVER
        self.SERVER = SERVER
        self.DATABASE = DATABASE
        self.UID = UID
        self.PWD = PWD
        conn_str = (
                'DRIVER=' + self.DRIVER + ';' +
                'SERVER=' + self.SERVER + ';' +
                'PORT=' + str(self.PORT) + ';' +
                'DATABASE=' + self.DATABASE + ';'
                'UID=' + self.UID + ';'
                'PWD=' + self.PWD
                )

        self._connection = pyodbc.connect(conn_str)        

        pyodbc.pooling = False
        engine_str = "mssql+pyodbc://" + self.UID + ":" + urllib.parse.quote_plus(self.PWD) + "@" + self.SERVER + ":"
        engine_str += str(self.PORT) + "/" + self.DATABASE
        engine_str += "?driver={}".format(urllib.parse.quote_plus(self.DRIVER))
        self.engine = sqlalchemy.create_engine(engine_str)

    def init_oracle(self, UID, PWD, SERVER='fmo8b.clemson.edu', PORT=1521, SID='AIM'):
        self.UID = UID
        self.PWD = PWD
        self.SERVER = SERVER
        self.PORT = PORT
        self.SID = SID
        #  conn_str = UID + '/' + PWD + '@'
        #  conn_str += "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(Host=" + SERVER + ")"
        #  conn_str += "(Port=" + str(PORT) + "))"
        #  conn_str += "(CONNECT_DATA=(SID=" + SID + ")))"
        #  self._connection = cx_Oracle.connect(conn_str)
        engine_str = "oracle://" + self.UID + ":" + urllib.parse.quote_plus(self.PWD) + "@" + self.SERVER + ":"
        engine_str += str(self.PORT) + "/" + self.SID
        self.engine = sqlalchemy.create_engine(engine_str)


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


