#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
import copy
import pandas as pd
from datetime import datetime
def create_live(self, connector):
    self.Tables['LATEST'].fetch_attributes(connector)
    Raw_TableName = self.Tables['LIVE'].Raw_TableName
    IDName = self.Tables['LATEST'].attributes['IDName']
    AliasName = self.Tables['LATEST'].attributes['AliasName']
    DateTimeName = self.Tables['LATEST'].attributes['DateTimeName']
    DataName = self.Tables['LATEST'].attributes['DataName']

    query = """
    IF OBJECT_ID('{}') IS NULL BEGIN
        CREATE TABLE {} (
            {} INT NOT NULL,
            {} DATETIME NOT NULL,
            {} FLOAT NOT NULL
        );
    END    
    """.format(Raw_TableName, Raw_TableName, IDName, DateTimeName, DataName)
    
    connector.exec_only(query)

    self.Tables['LIVE'].attributes = copy.deepcopy(self.Tables['LATEST'].attributes)
    self.Tables['LIVE'].attributes['Age'] = self.Tables['LIVE'].Age
    self.Tables['LIVE'].attributes['TableName'] = self.Tables['LIVE'].TableName
    self.Tables['LIVE'].attributes['Definition'] = query
    self.Tables['LIVE'].attributes['autoCACHE'] = 0
    self.Tables['LIVE'].attributes['autoLASR'] = 0
    self.Tables['LIVE'].attributes['Dependencies'] = None
    self.Tables['LIVE'].attributes['TableID'] = None

    self.Tables['LIVE'].register(connector)


def update_live(self, connector, metasys):
    IDName = self.Tables['LIVE'].attributes['IDName']
    DataName = self.Tables['LIVE'].attributes['DataName']
    DateTimeName = self.Tables['LIVE'].attributes['DateTimeName']

    query = """SELECT x.{}, m.ObjectID FROM {} AS x""".format(self.Tables['LIVE'].attributes['IDName'], self.XREF)
    query += """
    INNER JOIN CEVAC_PSID_OID_MAP AS m ON m.PointSliceID = x.{}
    """.format(IDName)
    
    psids = connector.exec_sql(query)
    live_df = pd.DataFrame({IDName:[],DateTimeName:[],DataName:[]})
    now = datetime.utcnow()
    for index, row in psids.iterrows():
        ObjectID = row['ObjectID']
        PointSliceID = row[IDName]
        pv = metasys.presentValue(ObjectID)
        df = pd.DataFrame({IDName:[PointSliceID],DateTimeName:[now],DataName:[pv]})
        print(df)
        live_df = live_df.append(df)
    connector.to_sql(live_df,name=self.Tables['LIVE'].Raw_TableName)

