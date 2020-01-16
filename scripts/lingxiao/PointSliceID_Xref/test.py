# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:35:51 2019

@author: suppe
"""
import bsql
import numpy as np

build_name = 'COOPER'
check_query = "SELECT BuildingSName FROM CEVAC_BUILDING_INFO ; "

#test_list = bsql.Query(check_query).json_list

a = [[1],[2],[3]]
a = np.reshape(a, len(a))[1:]
print(a)
