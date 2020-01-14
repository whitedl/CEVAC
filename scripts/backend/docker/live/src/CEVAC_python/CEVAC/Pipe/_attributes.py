#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

def fetch_attributes(self,connector):
    for k,t in self.Tables.items():
        t.fetch_attributes(connector)
        self.existingTables[t.Age] = t.exists(connector)
    self.attributes = self.Tables['HIST'].attributes
    
def fetch_points(self,connector):
    if len(self.attributes) == 0: self.fetch_attributes(connector)
    if self.existingTables['XREF']: ref = self.XREF
    else: ref = self.PXREF
    query = f"""
    SELECT x.{self.attributes['IDName']}, x.{self.attributes['AliasName']}, m.ObjectID, m.AttributeID
    FROM {ref} AS x
    INNER JOIN CEVAC_PSID_OID_MAP AS m ON m.PointSliceID = x.{self.attributes['IDName']}
    WHERE x.{self.attributes['IDName']} IS NOT NULL AND m.ObjectID IS NOT NULL
    """
    self.points = connector.exec_sql(query)
