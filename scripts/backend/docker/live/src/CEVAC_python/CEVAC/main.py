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
from funcs import *
import dateutil.parser

def main():
    wfic_cevac = SQLConnector(flavor="mssql")
    args = parse_arguments()
    if args.execute == "live":
        live(BuildingSName=args.BuildingSName, Metric=args.Metric, connector=wfic_cevac, loop=args.loop)

    if args.execute == "bootstrap":
        print('bootstrap')

    if args.execute == "psid_oid":
        build_psid_oid_map()

    if args.execute == "trend_samples":
        trend_samples(args.BuildingSName, args.Metric, connector=wfic_cevac,
                startTime=args.startTime, endTime=args.endTime)


def parse_arguments():
    parser = argparse.ArgumentParser(description="The CEVAC backend controller")
    parser.add_argument('-b','--BuildingSName',help="The standard BuildingSName")
    parser.add_argument('-m','--Metric',help="The standard Metric")
    parser.add_argument('-a','--Age',help="The standard Age")
    parser.add_argument('--startTime',help="")
    parser.add_argument('--endTime',help="")
    parser.add_argument('-x','--execute',help="Specify which method to execute")
    parser.add_argument('-l','--loop',action='store_true',help="Loop the specified action indefinitely")
    args = parser.parse_args()
    if args.BuildingSName != None:
        if ',' in args.BuildingSName:
            args.BuildingSName = args.BuildingSName.split(',')
    if args.Metric != None:
        if ',' in args.Metric:
            args.Metric = args.Metric.split(',')
    args.BuildingSName, args.Metric = make_lists(args.BuildingSName, args.Metric)
    if args.startTime != None:
        try:
            args.startTime = dateutil.parser.parse(args.startTime)
        except:
            print('Incorrectly formatted datetime')
    if args.endTime != None:
        try:
            args.endTime = dateutil.parser.parse(args.endTime)
        except:
            print('Incorrectly formatted datetime')

    return args

if __name__ == "__main__":
    main()
