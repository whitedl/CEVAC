#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Main backend process
"""
from CEVAC.Pipe import Pipe
from CEVAC.SQLConnector import SQLConnector
import argparse
from CEVAC.utils import *
from CEVAC.funcs import *
import dateutil.parser
exec_methods = {
    'live':live,
    'bootstrap':bootstrap,
    'trend_samples':trend_samples,
    'lasr_batch':lasr_batch,
    'psid_oid':build_psid_oid_map,
}
def main():
    wfic_cevac = SQLConnector(flavor="mssql")
    args = parse_arguments()
    args.__dict__['connector'] = wfic_cevac

    if args.execute in exec_methods: exec_methods[args.execute](**vars(args))

def parse_arguments():
    parser = argparse.ArgumentParser(description="The CEVAC backend controller")
    parser.add_argument('-b','--BuildingSName',help="The standard BuildingSName")
    parser.add_argument('-m','--Metric',help="The standard Metric")
    parser.add_argument('-a','--Age',help="The standard Age")
    parser.add_argument('--startTime',help="")
    parser.add_argument('--endTime',help="")
    parser.add_argument('-x','--execute',help="Specify which method to execute")
    parser.add_argument('-l','--loop',action='store_true',help="Loop the specified action indefinitely")
    parser.add_argument('--runsas',action='store_true',help="Run SAS Autoloader at the end of the script")
    parser.add_argument('--reset',action='store_true',help="Delete and rebuild the data set in /srv/csv/")
    parser.add_argument('--flush',action='store_true',help="Flush cache and transfer a fresh csv to SAS")
    parser.add_argument('--params',help="Parameters for CEVAC_TABLES columns")
    args = parser.parse_args()
    none_keys = []
    listable_args = ['BuildingSName', 'Metric', 'Age']
    for a in vars(args):
        val = getattr(args,a)
        if val is not None:
            if ',' in str(val) and a in listable_args:
                args.__dict__[a] = val.split(',')
        elif a != 'execute': none_keys.append(a)
    if args.params is not None: args.__dict__[a] = parse_params(val)
    args.BuildingSName, args.Metric, args.Age = make_lists(args.BuildingSName, args.Metric, args.Age)
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

    for a in none_keys: del args.__dict__[a] ## filter out None values
    return args

if __name__ == "__main__":
    main()
