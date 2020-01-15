#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

def fqr_lookup(self, fqr):
    p = {"fqr":fqr}
    rel = "objectIdentifiers"
    try:
        e = self.get(rel,params=p,raw=True)
    except:
        print('Error! Could not lookup fqr: ' + fqr)
        return None
    if "not found" in e:
        return None
    return e.strip("\"")


