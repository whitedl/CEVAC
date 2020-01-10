#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
from .Table import Table
from CEVAC import utils
class Pipe:
    from ._bootstrap import bootstrap
    from ._attributes import fetch_attributes
    from ._live import create_live
    from ._live import update_live
    def __init__(self,BuildingSName, Metric,isCustom=False):
        self.BuildingSName = BuildingSName
        self.Metric = Metric
        self.XREF = "CEVAC_" + self.BuildingSName + "_" + self.Metric + "_XREF"
        self.PXREF = "CEVAC_" + self.BuildingSName + "_" + self.Metric + "_PXREF"
        self.ages = ["PXREF","XREF","HIST","DAY","LATEST","LATEST_FULL",
                "LATEST_BROKEN","OLDEST", "LIVE"]
        self.isCustom = isCustom
        self.Tables = {}
        for a in self.ages:
            self.Tables[a] = Table(self.BuildingSName, self.Metric, a)

    def __getitem__(self, key):
        return self.Tables[key]

    def __delitem__(self, key):
        del self.Tables[key]

    
