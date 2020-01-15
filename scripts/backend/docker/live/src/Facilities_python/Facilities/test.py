#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
from MetasysConnector import MetasysConnector
from urllib import parse

def main():
    m = MetasysConnector()
    PointName = "ClemsonADX:WATT-CENTER/FC-1.UF1-11.ZN-T"
    #  PointName = "ClemsonADX:ACAD-SUCCESS/Field Bus1.VAV-115.ZN-T"
    #  PointName = "ClemsonADX:Hinson-Plant"
    #  PointName = "ClemsonADX:ACAD-SUCCESS"
    ObjectID = m.fqr_lookup(PointName)
    #  ObjectID = 'c72d1a58-3355-57a6-b9f1-e2e2d9c58db5'
    pv = m.presentValue(ObjectID)
    print(pv)
    #  print(ObjectID)
    #  children = m.getNetworkDeviceChildrenObjects(ObjectID)
    #  print(len(children['items']))
    #  for i in children['items']:
        #  print(i['itemReference'])
    #  attributes = m.getTrendedAttributes(ObjectID)
    #  print(attributes)
    #  samplesUrl = attributes['items'][0]['samplesUrl']
    #  print("samplesUrl:\n",samplesUrl)

    #  rel = "points/" + ObjectID + "/trendedAttributes"
    #  rel = "objects/" + ObjectID + "/trendedAttributes"
    #  out = m.get(rel)
    #  print(out)
    #  input()

    #  s = m.getTrendedAttributeSamples(ObjectID,85)
    #  v, t = None,None
    #  for i in s['items']:
        #  old_v = v
        #  v,t = i['value']['value'],i['timestamp']
        #  if v == old_v:
            #  continue
        #  else: print(v,t)

if __name__ == "__main__":
    main()
