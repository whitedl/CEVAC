#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Table
"""
class Table:
    from ._attributes import init_attributes
    def __init__(self, BuildingSName, Metric, Age, connector):
        self.BuildingSName = BuildingSName
        self.Metric = Metric
        self.Age = Age
        self.TableName = (
            'CEVAC_' + self.BuildingSName +
            '_' + self.Metric + 
            '_' + self.Age
        )
        self.init_attributes(connector)

