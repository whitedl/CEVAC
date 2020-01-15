#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

import datetime

def getTrendedAttributes(self,ObjectID):
    rel = "objects/" + ObjectID + "/trendedAttributes"
    e = self.get(rel)
    return e

def getTrendedAttributeSamples(self,ObjectID,attributeID,
        startTime=(datetime.datetime.utcnow() + datetime.timedelta(days=-7)),
        endTime=datetime.datetime.utcnow(),
        pageSize=10000, page=1):
    rel = "objects/" + ObjectID + "/attributes/" + str(attributeID) + "/samples"
    
    results,e = {}, {}
    
    while len(e) < pageSize and page < 100:
        params = {"startTime":startTime.isoformat(),
                "endTime": endTime.isoformat(),
                "pageSize":pageSize, "page":page}
        e = self.get(rel, params=params)
        results.update(e)
        page += 1

    return results

