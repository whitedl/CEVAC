#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Miscellaneous utilities
"""
import pandas as pd
from CEVAC.SQLConnector import SQLConnector
from Facilities import MetasysConnector
from CEVAC.Pipe import Pipe
import time
from multiprocessing import Process
from CEVAC.funcs import *

def build_psid_oid_map():
    wfic_cevac = SQLConnector(flavor='mssql')
    metasys = MetasysConnector()
    df = wfic_cevac.exec_sql("""
        SELECT DISTINCT TableName
        FROM CEVAC_TABLES
        WHERE TableName LIKE '%PXREF%'
        AND isCustom = 0
    """)
    psid_pn_df = pd.DataFrame({
        "PointSliceID":[],
        "PointName":[],
        })
    for i, row in df.iterrows():
        tn = row['TableName']
        query = "SELECT PointSliceID, LTRIM(RTRIM(PointName)) AS PointName FROM {}".format(tn)
        try:
            points_df = wfic_cevac.exec_sql(query)
            psid_pn_df = psid_pn_df.append(points_df)
        except:
            pass
    ObjectID_df = pd.DataFrame({
        "PointSliceID":[],
        "PointName":[],
        "ObjectID":[],
        "AttributeID":[]
        })
    seen_psids = []
    for index, row in psid_pn_df.iterrows():
        PointName, AttributeID = row['PointName'].split('.#')
        AttributeID = int(AttributeID)
        PointSliceID = row['PointSliceID']
        ObjectID = metasys.fqr_lookup(PointName)
        if PointSliceID in seen_psids:
            continue
        seen_psids.append(PointSliceID)
        r = pd.DataFrame({   
            "PointSliceID":[PointSliceID],
            "PointName":[PointName],
            "ObjectID":[ObjectID],
            "AttributeID":[AttributeID]
            })
        ObjectID_df = ObjectID_df.append(r)
    wfic_cevac.to_sql(ObjectID_df,name='CEVAC_PSID_OID_MAP')

def getPipes(BuildingSName=[],Metric=[],params={},connector=None) -> list:
    if connector == None: connector = SQLConnector(flavor='mssql')
    BuildingSName, Metric = make_lists(BuildingSName, Metric)
    query = """
    SELECT DISTINCT BuildingSName, Metric FROM CEVAC_TABLES
    WHERE TableName LIKE '%HIST_VIEW%'
    """
    if len(BuildingSName) > 0:
        query += "\n    AND BuildingSName IN ('"
        for b in BuildingSName: query += str(b) + "','"
        query = query[:-2] + ")"

    if len(Metric) > 0:
        query += "\n    AND Metric IN ('"
        for m in Metric: query += str(m) + "','"
        query = query[:-2] + ")"
    
    for k,v in params.items():
        query += f"\nAND {k} = '{v}'"

    pipes = []
    for i,r in connector.exec_sql(query).iterrows():
        pipes.append(Pipe(r['BuildingSName'], r['Metric']))

    return pipes
 
def live(BuildingSName=[], Metric=[], connector=None, metasys=None, loop=False, params={}, **kw):
    if connector == None: connector = SQLConnector(flavor='mssql')
    if metasys == None: metasys = MetasysConnector()
    params.update({'isCustom':0})
    pipes = getPipes(BuildingSName, Metric, params, connector=connector)
    run = True
    wait = False
    wait_msg, update_msg = "",""
    while run:
        for p in pipes:
            start = time.time()
            if not p.update_live(connector,metasys):
                if wait:
                    old_wait_msg = wait_msg
                    wait_msg = "Skipping " + str(p) + ". Too soon (" + str(p.last_now) + ")"
                    print(f'\r{wait_msg: <{len(old_wait_msg)}}',end="\r")
                    if end - time.time() < 1: time.sleep(1)
                continue
            end = time.time()
            wait = True
            old_update_msg = update_msg
            update_msg = "Updating " + str(p) + " took " + str(round(end-start,2)) + ' seconds (' + str(p.last_now) + ")"
            print(f'\r{update_msg: <{max(len(wait_msg),len(old_update_msg))}}',end="\n")
            run = loop

def trend_samples(BuildingSName=[], Metric=[], connector=None, metasys=None, startTime=None, endTime=None, **kw):
    if connector == None: connector = SQLConnector(flavor='mssql')
    if metasys == None: metasys = MetasysConnector()
    BuildingSName, Metric = make_lists(BuildingSName,Metric)
    pipes = getPipes(BuildingSName, Metric, {'isCustom':0}, connector=connector)
    for p in pipes:
        p.get_trend_samples(connector=connector,metasys=metasys,
                startTime=startTime, endTime=endTime)

def lasr_batch(BuildingSName=[], Metric=[], Age=[], connector=None,
        runsas=False, reset=False, flush=False, params={} 
        ):
    if connector == None: connector = SQLConnector(flavor='mssql')
    BuildingSName, Metric, Age = make_lists(BuildingSName, Metric, Age)
    pipes = getPipes(BuildingSName, Metric, params)
    ## append tables
    ## loop through pipes. if customLASR, run CREATE_VIEW for the HIST_LASR table
    ##   call lasr_append for the corresponding Age
    ##   pass runsas, reset, and flush to lasr_append

def lasr_append(BuildingSName=[], Metric=[], Age=[], connector=None,
        runsas=False, reset=False, flush=False):
    print('woah')

def bootstrap(**kw):
    print(kw)
