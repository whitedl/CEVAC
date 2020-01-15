#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

def register(self, connector, attributes=None):
    if attributes is not None:
        self.attributes = attributes
    query = """
    IF NOT EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = '{}') BEGIN
        INSERT INTO CEVAC_TABLES (
    """.format(self.TableName)
    for k in self.attributes:
        if k == "TableID":
            continue
        query += "\n        " + str(k) + ","
    ## remove trailing comma
    query = query[:-1]
    query += "\n) VALUES ("
    for k,v in self.attributes.items():
        if k == "Definition":
            v = v.replace("\'","\'\'")
        if k == "TableID":
            continue
        if v == 'True' or v == True:
            v = '1'
        if v == 'False' or v == False:
            v = '0'
        if v == None:
            query += "\n        NULL,"
        else:
            query += "\n        \'" + str(v) + "\',"
    query = query[:-1]
    query += ") END"
    try:
        self.create(connector)
    except Exception as e:
        print('Exception:')
        print(e)
        print('Aborting register')
    else:
        connector.exec_only(query)
        self.fetch_attributes(connector)

def update_attributes(self, connector):
    if self.exists(connector):
        query = """
        UPDATE CEVAC_TABLES
        """

def create(self, connector):
    if not self.exists(connector,check=['dbo']):
        try:
            connector.exec_only(self.attributes['Definition'])
        except:
            print('Failed to create table',self.TableName)
            print('Definition:')
            print(self.attributes['Definition'])
    else:
        print(self.TableName,'already exists')
