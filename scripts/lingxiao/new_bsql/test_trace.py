from new_bsql import *
import numpy as np
import pandas as pd
import json

test_query = "SELECT DISTINCT TableName, Definition FROM CEVAC_TABLES WHERE isCustom = 1 AND TableName LIKE '%HIST_VIEW%'"
test_data = new_bsql().RequestData(test_query)
#print(test_data)

df = new_bsql().RequestDataframe(test_query)
print(df)

'''
with open("test.json", "w") as f:
    json.dump(df,f)
'''
#new_bsql().RequestData_csv(test_query, 'table_definition.csv')

print(df.iloc[0][1])