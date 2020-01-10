#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
import copy
import pandas as pd
from datetime import datetime
from multiprocessing import Pool, cpu_count
from functools import partial

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

def pv(metasys,o_ID):
    return metasys.presentValue(o_ID)

def update_live(self, connector, metasys):
    if not self.Tables['LIVE'].exists:
        self.create_live()

    self.Tables['LIVE'].fetch_attributes(connector)
    IDName = self.Tables['LIVE'].attributes['IDName']
    DataName = self.Tables['LIVE'].attributes['DataName']
    DateTimeName = self.Tables['LIVE'].attributes['DateTimeName']
    if self.Tables['XREF'].exists(connector):
        ref = self.XREF
    else:
        ref = self.PXREF

    query = "SELECT x.{}, m.ObjectID FROM {} AS x".format(self.Tables['LIVE'].attributes['IDName'], ref)
    query += "\n INNER JOIN CEVAC_PSID_OID_MAP AS m ON m.PointSliceID = x.{}".format(IDName)
    query += "\n WHERE x.{} IS NOT NULL AND m.ObjectID IS NOT NULL".format(IDName)
    
    psids = connector.exec_sql(query)
    live_df = pd.DataFrame({IDName:[],DateTimeName:[],DataName:[]})
    now = datetime.utcnow()
    ObjectIDs = psids['ObjectID'].values.tolist()
    func = partial(pv,metasys)

    p = Pool(cpu_count())
    result = p.map(func,ObjectIDs)
    p.close()
    p.join()

    for index, row in psids.iterrows():
        ObjectID = row['ObjectID']
        PointSliceID = row[IDName]
        v = result[index]
        df = pd.DataFrame({IDName:[PointSliceID],DateTimeName:[now],DataName:[v]})
        live_df = live_df.append(df)
    connector.to_sql(live_df,name=self.Tables['LIVE'].Raw_TableName)

