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
    fmo8b = SQLConnector(flavor='oracle')
    wfic_cevac = SQLConnector(flavor='mssql')
    #  query = "SELECT * FROM test"
    #  df = wfic_cevac.exec_sql(query)
    #  print(df)
    query = 'SELECT * FROM FAC.CEVAC_TICKETS'
    out = fmo8b.exec_sql(query)
    wfic_cevac.to_sql(out, name='TEST_DF')
    
    #  t = Table('WATT','TEMP','LATEST',connector)
    #  print(t.attributes['autoCACHE'])
    #  a = AgeSet('WATT','TEMP','HIST',connector)


if __name__ == "__main__":
    main()
