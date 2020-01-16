#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

def bootstrap(self):
    ## check XREF for setpoints
    ## check for 'ReadingType' in XREF for customLASR
    ##   ask user to create HIST_LASR
    ## check if exists
    ## check for custom (read /cevac/CUSTOM_DEFS/{TableName}.sql) or isCustom
    ##   ask user to reuse previous structure or to reload
    ## 
    ## PHASE 1  :  delete everything
    ## PHASE 2  :  insert into CEVAC_TABLES
    ## PHASE 3  :  if cache, init cache
    ## PHASE 3.5:  if customLASR, create HIST_LASR
    ## PHASE 4  :  create CSVs and rsync to LASR (HIST, LATEST (if no live), XREF)
    print('TODO')
    ## 
