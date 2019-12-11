#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Table
"""
class Table:
    from ._attributes import fetch_attributes
    from ._register import register
    def __init__(self, BuildingSName, Metric, Age):
        self.BuildingSName = BuildingSName
        self.Metric = Metric
        self.Age = Age
        self.TableName = (
            'CEVAC_' + self.BuildingSName +
            '_' + self.Metric + 
            '_' + self.Age
        )
        self.SourceTable = self.TableName + "_VIEW"
        self.CacheTable = self.TableName + "_CACHE"
        self.Raw_TableName = self.TableName + "_RAW"
        self.attributes = {}

