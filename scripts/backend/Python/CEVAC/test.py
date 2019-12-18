#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
"""
from SQLConnector import SQLConnector
from Pipe import Pipe
#  import json
#  from Table import Table
#  from AgeSet import AgeSet

def main():
    #  fmo8b = SQLConnector(flavor='oracle')
    wfic_cevac = SQLConnector(flavor='mssql')
    p = Pipe('FIKE','HUM')
    print(p.Tables['XREF'].exists(wfic_cevac))

if __name__ == "__main__":
    main()
