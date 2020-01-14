#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

def fetch_attributes(self,connector):
    query = (
        "SELECT TOP 1 * FROM CEVAC_TABLES WHERE TableName = '"
        + self.TableName + "'" 
        )
    a = connector.exec_sql(query)
    self.attributes = {}
    if len(a.index) > 0:
        for k in a:
            self.attributes[k] = a[k][0]

def exists(self,connector, check=['dbo','CEVAC_TABLES']):
    exists = True
    ## check if table exists in the db
    if 'dbo' in check:
        query = "IF OBJECT_ID('{}') IS NOT NULL SELECT 'exists' ELSE SELECT 'dne'".format(self.TableName)
        dbo_str = connector.sql_value(query)
        dbo = False
        if dbo_str == "exists":
            dbo = True
        exists = exists and dbo
    ## check if table has entry in CEVAC_TABLES
    if 'CEVAC_TABLES' in check:
        query = """
        IF EXISTS(SELECT TableName FROM CEVAC_TABLES WHERE TableName = '{}') SELECT 'exists'
        ELSE SELECT 'dne'
        """.format(self.TableName)
        cevac_tables_str = connector.sql_value(query)
        cevac_tables = False
        if cevac_tables_str == "exists":
            cevac_tables = True
        exists = exists and cevac_tables

    return exists

