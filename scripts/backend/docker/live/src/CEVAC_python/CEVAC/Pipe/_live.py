#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
import copy
import pandas as pd
import datetime
from multiprocessing import Pool, cpu_count
from functools import partial
import subprocess as sub
from funcs import *

def pv(metasys,o_ID):
    return metasys.presentValue(o_ID)

def update_live(self, connector, metasys):
    now = roundTime(datetime.datetime.utcnow(),datetime.timedelta(minutes=1))
    if self.last_now == now:
        return False
    self.last_now = now

    if len(self.attributes) == 0: self.fetch_attributes(connector)
    #  if not self.Tables['LIVE'].exists(connector):
    if not self.existingTables['LIVE']:
        self.create_table('LIVE',templateAge='LATEST',connector=connector)

    IDName = self.Tables['LIVE'].attributes['IDName']
    DataName = self.Tables['LIVE'].attributes['DataName']
    DateTimeName = self.Tables['LIVE'].attributes['DateTimeName']
    if self.existingTables['XREF']:
        ref = self.XREF
    else:
        ref = self.PXREF

    query = "SELECT x.{}, m.ObjectID FROM {} AS x".format(self.Tables['LIVE'].attributes['IDName'], ref)
    query += "\n INNER JOIN CEVAC_PSID_OID_MAP AS m ON m.PointSliceID = x.{}".format(IDName)
    query += "\n WHERE x.{} IS NOT NULL AND m.ObjectID IS NOT NULL".format(IDName)
    
    if self.points is None: self.fetch_points(connector)
    #  psids = connector.exec_sql(query)
    live_df = pd.DataFrame({IDName:[],DateTimeName:[],DataName:[]})
    ObjectIDs = self.points['ObjectID'].values.tolist()
    func = partial(pv,metasys)
    p = Pool(cpu_count())
    result = p.map(func,ObjectIDs)
    p.close()
    p.join()

    for index, row in self.points.iterrows():
        ObjectID = row['ObjectID']
        PointSliceID = row[IDName]
        v = result[index]
        df = pd.DataFrame({IDName:[PointSliceID],DateTimeName:[now],DataName:[v]})
        live_df = live_df.append(df)
    connector.to_sql(live_df,name=self.Tables['LIVE'].Raw_TableName)
    #  print(self.BuildingSName,' ', self.Metric)
    #  print('checking alert queue')
    #  input()
    #  self.checkAlertQueue(connector)
    return True

def checkAlertQueue(self, connector, host="wfic-cevac1", user="cevac"):
    q = f"INSERT INTO CEVAC_ALERT_QUEUE (BuildingSName, Metric, Age) VALUES ('{self.BuildingSName}','{self.Metric}','LIVE');"
    connector.exec_only(q)
    command = "/cevac/scripts/checkAlertQueue.sh"
    sub.Popen(["ssh", f"{user}@{host}", command])

