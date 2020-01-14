#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
from .Table import Table
class Pipe:
    from ._bootstrap import bootstrap
    from ._delete import delete
    from ._attributes import fetch_attributes, fetch_points
    from ._live import update_live, checkAlertQueue
    from ._trend_samples import get_trend_samples
    from ._create import create_table
    def __init__(self,BuildingSName, Metric,isCustom=False):
        self.BuildingSName = BuildingSName
        self.Metric = Metric
        self.XREF = "CEVAC_" + self.BuildingSName + "_" + self.Metric + "_XREF"
        self.PXREF = "CEVAC_" + self.BuildingSName + "_" + self.Metric + "_PXREF"
        self.ages = ["PXREF","XREF","HIST","DAY","LATEST","LATEST_FULL",
                "LATEST_BROKEN","OLDEST", "LIVE", "TREND"]
        self.isCustom = isCustom
        self.last_now = None
        self.Tables = {}
        self.attributes = {}
        self.existingTables = {}
        self.points = None
        for a in self.ages:
            self.Tables[a] = Table(self.BuildingSName, self.Metric, a)

    def __getitem__(self, key):
        return self.Tables[key]

    def __delitem__(self, key):
        del self.Tables[key]

    def __str__(self):
        return self.BuildingSName + '_' + self.Metric
    
    def __repr__(self):
        return str(self)
        #  return ("╠" + self.BuildingSName + '_' + self.Metric + "╣").encode('utf-8')
    
