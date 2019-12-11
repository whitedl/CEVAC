#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Main backend process
"""
from Pipe import Pipe
from SQLConnector import SQLConnector
import argparse
from utils import *

def main():
    wfic_cevac = SQLConnector(flavor="mssql")
    args()
    #  p = Pipe('WATT','TEMP')
    #  p.bootstrap()
    #  p.fetch_attributes(wfic_cevac)
    #  print(p['DAY'].attributes)

def args(connector=None):
    parser = argparse.ArgumentParser(description="The CEVAC backend controller")
    parser.add_argument('-b','--BuildingSName',help="The standard BuildingSName")
    parser.add_argument('-m','--Metric',help="The standard Metric")
    parser.add_argument('-a','--Age',help="The standard Age")
    parser.add_argument('-x','--execute',help="Specify which method to execute")
    args = parser.parse_args()

    def require_bsn_and_metric(args):
        valid = True
        if args.BuildingSName is None:
            print('Missing BuildingSName. Run again with -b or --BuildingSName')
            valid = False
        if args.Metric is None:
            print('Missing Metric. Run again with -m or --Metric')
            valid = False
        return valid

    if args.execute == "live":
        if require_bsn_and_metric(args):
            live(args.BuildingSName, args.Metric, connector=connector)

    if args.execute == "bootstrap":
        print('bootstrap')


if __name__ == "__main__":
    main()
