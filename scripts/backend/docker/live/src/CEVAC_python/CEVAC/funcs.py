#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import datetime

def make_lists(*tup):
    args = list(tup)
    for i,a in enumerate(args):
        if a is None:
            args[i] = []
            continue
        if not isinstance(a, list): args[i] = [a]
    return tuple(args)

def gen_TableName(BuildingSName, Metric, Age=None):
    TableName = "CEVAC_" + BuildingSName + "_" + Metric
    if Age is not None:
        TableName += "_" + Age
    return TableName

def roundTime(dt=None, dateDelta=datetime.timedelta(minutes=1)):
    roundTo = dateDelta.total_seconds()
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


