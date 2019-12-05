#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
"""
from Table import Table

class AgeSet:
    def __init__(self, BuildingSName, Metric, Age, connector):
        self.sourceTable = Table(BuildingSName, Metric, Age, connector)
        
