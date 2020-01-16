#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
"""
from CEVAC.SQLConnector import SQLConnector
from CEVAC.SASConnector import SASConnector
from CEVAC.Pipe import Pipe
from Facilities import MetasysConnector
#  import json
#  from Table import Table
#  from AgeSet import AgeSet

def main():
    #  m = MetasysConnector()
    #  fmo8b = SQLConnector(flavor='oracle')
    wfic_cevac = SQLConnector(flavor='mssql')
    #  sas = SASConnector()
    #  sas.execute('touch deleteme.txt')
    p = Pipe('FIKE','WIND')
    p.fetch_attributes(wfic_cevac)
    print(p.attributes)
    p['HIST'].register(wfic_cevac,update=True)
    

if __name__ == "__main__":
    main()
