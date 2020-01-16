#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

#  import pyodbc
import sqlalchemy
import cx_Oracle
import urllib.parse
from CEVAC.config import config as cf

class SQLConnector():
    from ._cursor import cursor
    from ._exec_sql import exec_sql, to_sql, sql_value, exec_only

    def __init__(self, flavor='mssql', index=0):
        self.engine = None
        self.flavor = flavor
        self.__dict__.update(cf['SQLConnector'][flavor][index])
        self.create_engine()

    def create_engine(self, port=1433, driver='ODBC Driver 17 for SQL Server'):
        if not hasattr(self, 'port'): self.port = port
        if not hasattr(self, 'driver'): self.driver = driver
        ### conn_str is not needed because we are using sqlalchemy,
        ### but it's a pain to write, so I'm leaving it in
        #  conn_str = (
                #  'DRIVER=' + self.driver + ';' +
                #  'SERVER=' + self.host + ';' +
                #  'PORT=' + str(self.port) + ';' +
                #  'DATABASE=' + self.database + ';'
                #  'UID=' + self.username + ';'
                #  'PWD=' + self.password
                #  )
        #  self._connection = pyodbc.connect(conn_str)        
        #  pyodbc.pooling = False
        if self.flavor == "mssql": engine_driver = "mssql+pyodbc"
        elif self.flavor == "oracle":
            engine_driver = "oracle+cx_oracle"
            try:
                self.database = self.sid
            except:
                print('sid not set in config.yaml')
        elif self.flavor != "sqlite":
            engine_driver = self.flavor
        engine_str = (
            f"{engine_driver}://{self.username}:{urllib.parse.quote_plus(self.password)}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        if hasattr(self,'driver'): engine_str += f"?driver={urllib.parse.quote_plus(self.driver)}"
        if self.flavor == "sqlite": engine_str = "sqlite:///{self.database}.sqlite"
        self.engine = sqlalchemy.create_engine(engine_str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

    def __repr__(self):
        return "TODO"

    def __str__(self):
        return "TODO"

    #  def __del__(self):
        #  self._connection.close()

