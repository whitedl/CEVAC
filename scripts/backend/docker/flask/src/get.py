#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Miscellaneous GET requests live here
"""
import CEVAC
from flask import request

def clean_args(req_args):
    args = {}
    args.update(req_args)
    for k in args:
        if args[k] == '':
            args[k] = None
    return args


def bin_value(BuildingSName=None, Metric=None, column=None, connector=None):
    query = f"""
    IF EXISTS(
      SELECT {column} FROM CEVAC_TABLES
      WHERE {column} = 1
      AND BuildingSName = '{BuildingSName}'
      AND Metric = '{Metric}'
    ) SELECT '1' AS e
    ELSE SELECT '0' AS e
    """
    return connector.sql_value(query)

def building_info(connector=None):
    query = """
    SELECT BuildingSName, BuildingDName, BuildingKey, ReportLink
    FROM CEVAC_BUILDING_INFO AS bi
    ORDER BY BuildingSName ASC
    """
    df = connector.exec_sql(query)
    out = """
    <tr>
      <th></th>
      <th>BuildingSName</th>
      <th>BuildingDName</th>
      <th>BuildingKey</th>
      <th>ReportLink</th>
    </tr>
    """
    for i, r in df.iterrows():
        out += f"""
        <tr>
        <td><a onclick='delete_building_link_click(\""{r['BuildingSName']}"\")' class='delete_building_link' id='delete_building_link_{r['BuildingSName']}'>delete</a></td>
          <td contenteditable='true'>{r['BuildingSName']}</td>
          <td contenteditable='true'>{r['BuildingDName']}</td>
          <td contenteditable='true'>{r['BuildingKey']}</td>
          <td contenteditable='true'>{r['ReportLink']}</td>
        </tr>
        """
    return out

def table_html(BuildingSName=None, Metric=None, Age=None, TableName=None, editable=False, order_by=None, connector=None):
    if connector is None: connector = CEVAC.Connectors.SQLConnector(flavor='mssql')
    t = CEVAC.Pipe.Table(BuildingSName, Metric, Age, connector=connector)
    return t.html(editable=editable, order_by=order_by)
