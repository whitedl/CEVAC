#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

def getNetworkDevices(self,pageSize=1000):
    rel = "networkDevices"
    params = {"pageSize":pageSize}
    e = self.get(rel,params=params)
    return e

def getNetworkDeviceChildren(self,ObjectID):
    rel = "networkDevices/" + ObjectID + "/networkDevices"
    e = self.get(rel)
    return e

def getNetworkDeviceChildrenObjects(self,ObjectID,pageSize=1000,sort="itemReference"):
    rel = "networkDevices/" + ObjectID + "/objects"
    params = {"pageSize": pageSize, "sort":sort}
    e = self.get(rel,params=params)
    return e
