# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:35:51 2019

@author: suppe
"""
import numpy as np
import bsql

build_name = 'COOPER'
check_query = "SELECT BuildingSName FROM CEVAC_BUILDING_INFO;"
check_query_2 = "SELECT Metric FROM CEVAC_METRIC; "
test_q = bsql.Query(check_query)
test_q_m = bsql.Query(check_query_2)

res = test_q.json_list[1:]
#print(res)
res_m = test_q_m.json_list

building_list = np.reshape(res, len(res))
metric_list = np.reshape(res_m, len(res_m))
print(building_list)
if build_name in building_list:
    print('True')
else:
    print('False')

print(metric_list)


'''
import db_drive

test_obj = db_drive.db_obj

command = "select BuildingSName from CEVAC_BUILDING_INFO;"

res = test_obj.get_data(command)
print(res)
'''
