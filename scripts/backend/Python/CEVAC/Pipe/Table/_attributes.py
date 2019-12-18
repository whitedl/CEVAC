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

def exists(self,connector):
    query = "IF OBJECT_ID('{}') IS NOT NULL SELECT 'exists' ELSE SELECT 'dne'".format(self.TableName)
    exists_str = connector.sql_value(query)
    exists = False
    if exists_str == "exists":
        exists = True
    return exists
