#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Miscellaneous utilities
"""
import pandas as pd
from SQLConnector import SQLConnector
from Facilities import MetasysConnector
from Pipe import Pipe

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
        "ObjectID":[]
        })
    seen_psids = []
    for index, row in psid_pn_df.iterrows():
        PointName = row['PointName'].strip('.#85')
        PointSliceID = row['PointSliceID']
        ObjectID = metasys.fqr_lookup(PointName)
        if PointSliceID in seen_psids:
            continue
        seen_psids.append(PointSliceID)
        r = pd.DataFrame({   
            "PointSliceID":[PointSliceID],
            "PointName":[PointName],
            "ObjectID":[ObjectID]
            })
        ObjectID_df = ObjectID_df.append(r)
    wfic_cevac.to_sql(ObjectID_df,name='CEVAC_POINTSLICEID_OBJECTID_MAP')

def gen_TableName(BuildingSName, Metric, Age=None):
    TableName = "CEVAC_" + BuildingSName + "_" + Metric
    if Age is not None:
        TableName += "_" + Age
    return TableName

def live(BuildingSName, Metric, connector=None, metasys=None):
    if connector == None:
        connector = SQLConnector(flavor='mssql')
    if metasys == None:
        metasys = MetasysConnector()
    p = Pipe(BuildingSName, Metric)
    p.create_live(connector)
    p.update_live(connector,metasys)

#  if __name__ == "__main__":
    #  build_psid_oid()
