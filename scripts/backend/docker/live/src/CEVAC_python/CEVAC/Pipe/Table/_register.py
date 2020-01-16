#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

def register(self, connector, attributes=None, update=False):
    if attributes is not None:
        self.attributes = attributes
    if not update:
        if self.exists(connector): update = True
        else: update = False

    def attribute_parse(k):
        v = self.attributes[k]
        if k == "Definition": v = v.replace("\'","\'\'").lstrip()
        elif k == "TableID": return None
        elif v == 'True' or v == True: v = '1'
        elif v == 'False' or v == False: v = '0'
        elif v == None: vals += "\nNULL,"
        return v
    def attributes_columns():
        cols = ""
        for k in self.attributes:
            if k == "TableID": continue
            cols += "\n" + str(k) + ","
        return cols[:-1]

    def attributes_values():
        vals = ""
        for k,v in self.attributes.items():
            v = attribute_parse(k)
            if v is None: continue
            else: vals += "\n\'" + str(v) + "\',"
        return vals[:-1]

    if not update:
        query = ("INSERT INTO CEVAC_TABLES (" + attributes_columns()
                + "\n) VALUES (" + attributes_values() + ")")
    else:
        query = "UPDATE CEVAC_TABLES SET "
        for k,v in self.attributes.items():        
            v = attribute_parse(k)
            if v is not None: query += "\n" + str(k) + " = \'" + attribute_parse(k) + "\',"
        query = query[:-1]

    if not update:
        try:
            self.create(connector)
        except Exception as e:
            print('Exception:')
            print(e)
            print('Aborting register')
        else:
            connector.exec_only(query)
            self.fetch_attributes(connector)
    else:
        try:
            connector.exec_only(query)
        except:
            print('Failed to update' + self.TableName)
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
