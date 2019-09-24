"""Import work orders."""

from pandas import read_excel, isna
from os import listdir
import datetime


DEBUG = True
SEND = False

READ_DIR = "/home/hchall/"


def list_to_comma_seperated_values(some_list):
    """Return list of comma seperated values."""
    csv = ""
    for i in some_list:
        if i in ["NULL"]:
            csv += f"{i},",
        else:
            csv += f"'{i}',"
    return csv[:-1]


import_files = []
for file in listdir(READ_DIR):
    if file.endswith(".xlsx"):
        import_files.append(file)

insert_sql_total = ""
for file in import_files:
    document = read_excel(READ_DIR + file)
    headers = [head for head in document]
    print(headers)
    for i in range(len(document)):
        try:
            values = ['']*len(headers)
            for j, header in enumerate(headers):
                if isna(document[header][i]):
                    values[j] = "NULL"
                elif j in [8, 14]:  # Date in format 31-JAN-19
                    some_date = datetime.datetime.strptime(document[header][i],
                                                           '%d-%b-%y')
                    values[j] = some_date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    values[j] = str(document[header][i])

            insert_sql = (f"INSERT INTO X ("
                          f"{list_to_comma_seperated_values(headers)}"
                          f") VALUES ("
                          f"{list_to_comma_seperated_values(values)}"
                          f")\nGO\n")
            insert_sql_total += insert_sql
        except Exception as e:
            print(values)
            print(e.traceback())
            print(f"No data {Exception}")

    # print(insert_sql_total)
