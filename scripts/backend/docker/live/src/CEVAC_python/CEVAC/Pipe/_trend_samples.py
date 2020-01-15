#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

import pandas as pd
from Facilities import MetasysConnector
from SQLConnector import SQLConnector
import dateutil.parser
import datetime
from funcs import *
from functools import partial
from multiprocessing import Pool, cpu_count

def samples(metasys : MetasysConnector, IDName : str, DateTimeName : str, DataName : str,
        startTime : datetime.datetime, endTime : datetime.datetime, PointSliceID : int,
        ObjectID : str, AttributeID : int):
    s = metasys.getTrendedAttributeSamples(ObjectID, int(AttributeID),startTime=startTime, endTime=endTime)
    t_df = pd.DataFrame({IDName:[],DateTimeName:[],DataName:[]})
    v, t = None, None
    for i in s['items']:
        old_v = v
        v, t = i['value']['value'], dateutil.parser.parse(i['timestamp'])
        if v == old_v: continue
        t = t.replace(tzinfo=None)
        t = roundTime(t)
        df = pd.DataFrame({IDName:[PointSliceID],DateTimeName:[t],DataName:[v]})
        t_df = t_df.append(df,ignore_index=True)
    return t_df

def get_trend_samples(self,connector=None,metasys=None,
        startTime=datetime.datetime.utcnow() - datetime.timedelta(1),
        endTime=datetime.datetime.utcnow()):
    if startTime is None: startTime = datetime.datetime.utcnow() - datetime.timedelta(1)
    if endTime is None: endTime = datetime.datetime.utcnow()
    if self.points is None: self.fetch_points(connector)
    if connector is None: connector = SQLConnector(flavor='mssql')
    if metasys is None: metasys = MetasysConnector()
    if not self.existingTables['TREND']: self.create_table('TREND',templateAge='HIST',connector=connector)
    IDName = self.Tables['TREND'].attributes['IDName']
    DateTimeName = self.Tables['TREND'].attributes['DateTimeName']
    DataName = self.Tables['TREND'].attributes['DataName']
    AliasName = self.Tables['TREND'].attributes['AliasName']
    trend_df = pd.DataFrame({IDName:[],DateTimeName:[],DataName:[]})

    args = []
    for index, row in self.points.iterrows():
        args.append((metasys,
            IDName, DateTimeName, DataName,
            startTime,endTime,
            row['PointSliceID'],
            row['ObjectID'],
            row['AttributeID']))
    p = Pool(cpu_count())
    result = p.starmap(samples,args)
    p.close()
    p.join()

    for r in result:
        trend_df = trend_df.append(r)
    connector.to_sql(trend_df,name=self.Tables['TREND'].Raw_TableName)
