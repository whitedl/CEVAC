#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
TODO Add definitions for all Ages
"""

def definition(self,standard=True):
    definition = ""
    if standard:
        PXREF = 'CEVAC_' + self.BuildingSName + '_' + self.Metric + '_PXREF'
        definition = f"""
        CREATE VIEW {self.attributes['TableName']} AS
        SELECT px.{self.attributes['IDName']},
            px.{self.attributes['AliasName']},
            raw.{self.attributes['DateTimeName']},
            dbo.ConvertUTCToLocal(raw.{self.attributes['DateTimeName']}) AS ETDateTime,
            raw.{self.attributes['DataName']}
        FROM {self.Raw_TableName} AS raw
        INNER JOIN {PXREF} AS px ON px.{self.attributes['IDName']} = raw.{self.attributes['IDName']}
        """
    self.attributes['Definition'] = definition
