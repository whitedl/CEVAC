import re

#test_str = "select * from CEVAC_ERRORS order by CEVAC_WATT_POWER_HIST by UTCDateTime desc"
#test_str = str(('42S22', "[42S22] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Invalid column name 'error_test'. (207) (SQLExecDirectW)"))
test_str = "select * from test"
#pattern = re.compile(r"CEVAC\S+")
#pattern = re.compile(r"CEVAC.+?\s")
#pattern = re.compile(r"].+?\)")
pattern = re.compile(r"from+\s")
match = pattern.search(test_str)

if match:
    print(match)

else:
    print("no thing")