#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

def presentValue(self, ObjectID):
    rel = "objects/" + ObjectID + '/attributes/' + 'presentValue'
    e = self.get(rel)
    try:
        pv = e['item']['presentValue']['value']
    except:
        return None
    else:
        return pv

