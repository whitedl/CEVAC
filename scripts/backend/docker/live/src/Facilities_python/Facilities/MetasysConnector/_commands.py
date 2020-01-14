#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

def getCommands(self, ObjectID):
    rel = "objects/" + ObjectID + '/commands'
    e = self.get(rel)
    return e
