#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

def init_attributes(self,connector):
    query = (
        "SELECT TOP 1 * FROM CEVAC_TABLES WHERE TableName = '"
        + self.TableName + "'" 
        )
    a = connector.exec_sql(query)
    self.attributes = {}
    for k in a:
        self.attributes[k] = a[k][0]

