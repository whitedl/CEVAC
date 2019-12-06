#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
"""
from SQLConnector import SQLConnector
import json
from Table import Table
from AgeSet import AgeSet

def main():
    connector = SQLConnector(oracle=True)
    query = 'SELECT * FROM FAC.CEVAC_DAILY_WO'
    out = connector.exec_sql(query)
    csv = out.to_csv(index=False)
    print(csv)
    #  t = Table('WATT','TEMP','LATEST',connector)
    #  print(t.attributes['autoCACHE'])
    #  a = AgeSet('WATT','TEMP','HIST',connector)


if __name__ == "__main__":
    main()
