#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""
import copy
from CEVAC.funcs import *
def create_table(self,Age,templateAge='HIST',connector=None,has_raw=True,standard=True):
    if len(self.Tables[templateAge].attributes) == 0: self.Tables[templateAge].fetch_attributes(connector)
    if connector is None: connector = SQLConnector(flavor='mssql')
    Raw_TableName = self.Tables[Age].Raw_TableName
    IDName = self.Tables[templateAge].attributes['IDName']
    AliasName = self.Tables[templateAge].attributes['AliasName']
    DateTimeName = self.Tables[templateAge].attributes['DateTimeName']
    DataName = self.Tables[templateAge].attributes['DataName']

    query = f"""
    IF OBJECT_ID('{Raw_TableName}') IS NULL BEGIN
        CREATE TABLE {Raw_TableName} (
            {IDName} INT NOT NULL,
            {DateTimeName} DATETIME NOT NULL,
            {DataName} FLOAT NOT NULL
        );
    END    
    """
    if has_raw: connector.exec_only(query)

    self.Tables[Age].attributes = copy.deepcopy(self.Tables[templateAge].attributes)
    self.Tables[Age].attributes['Age'] = self.Tables[templateAge].Age
    self.Tables[Age].attributes['TableName'] = gen_TableName(self.BuildingSName, self.Metric,Age)
    self.Tables[Age].definition(standard=standard)
    self.Tables[Age].attributes['autoCACHE'] = 0
    self.Tables[Age].attributes['autoLASR'] = 0
    self.Tables[Age].attributes['Dependencies'] = Raw_TableName
    self.Tables[Age].attributes['TableID'] = None

    self.Tables[Age].register(connector)

