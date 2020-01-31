#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
This module is for generating html
"""

def buildings_select_html(connector=None, **kw):
    query = """
    SELECT DISTINCT BuildingSName, BuildingDName
    FROM CEVAC_BUILDING_INFO
    ORDER BY BuildingDName ASC
    """
    df = connector.exec_sql(query)
    out = ""
    for i, r in df.iterrows():
        out += f"<option value=\'{r['BuildingSName']}\'>{r['BuildingDName']}</option>"
    return out

def metrics_select_html(BuildingSName=None, fil=None, connector=None, **kw):
    if fil == "existing":
        query = f"""
        SELECT DISTINCT RTRIM(ct.Metric) AS Metric, ISNULL(um.DisplayNameShort, 'No units') AS dn
        FROM CEVAC_TABLES AS ct
        LEFT OUTER JOIN CEVAC_METRIC AS cm ON cm.Metric = ct.Metric
        LEFT OUTER JOIN tblUnitOfMeasure AS um ON um.UnitOfMeasureID = cm.unitOfMeasureID
        WHERE BuildingSName = '{BuildingSName}'
        AND Age = 'HIST'
        """
    else:
        query = """
        SELECT DISTINCT RTRIM(cm.Metric) AS Metric, ISNULL(um.DisplayNameShort, 'No units') AS dn
        FROM CEVAC_METRIC AS cm
        LEFT OUTER JOIN tblUnitOfMeasure AS um ON um.UnitOfMeasureID = cm.unitOfMeasureID
        """
    df = connector.exec_sql(query)
    out = ""
    for i, r in df.iterrows():
        out += f"<option value=\'{r['Metric']}\'>{r['Metric']} ({r['dn']})</option>"
    return out


