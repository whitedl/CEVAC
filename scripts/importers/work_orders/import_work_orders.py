"""Import work orders."""

from pandas import read_excel, isna
from os import listdir
import datetime
import time
import os
from stat import S_ISREG


DEBUG = True
SEND = False

READ_DIR = "/home/hchall/"
PROCESSED_DIR = "/home/hchall/"

d = {'FIKE RECREATION CENTER ': 'FIKE',
     'RIGGS HALL ': 'RIGGS',
     'COOPER LIBRARY ': 'COOPER',
     'LITTLEJOHN COLISEUM ': 'LITTLEJOHN',
     'FLUOR DANIEL (ENGINEERING INNOVATION CENTER) EIB': 'FLUOR',
     'ACADEMIC SUCCESS CENTER': 'ASC',
     'LEE HALL ADDITION / LEE III': 'LEE_III',
     'WATT FAMILY INNOVATION CENTER': 'WATT',
     'MCCABE HALL ': 'MCCABE'}


def list_to_comma_seperated_values(some_list):
    """Return list of comma seperated values."""
    csv = ""
    for i in some_list:
        if i in ["NULL"]:  # No apostrophes on NULL
            csv += f"{i},"
        else:
            csv += f"\'{i}\',"
    return csv[:-1]  # Remove last comma


def cleanup(some_dir):
    """Remove files older than 2 weeks."""
    now = time.time()
    keep_period = 1209600  # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [some_dir]:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if (S_ISREG(os.stat(fpath).st_mode) and
                    os.path.getatime(fpath) < cutoff):
                os.remove(fpath)


import_files = []
for file in listdir(READ_DIR):
    if file.endswith(".xlsx"):
        import_files.append(file)

insert_sql_total = ""
for file in import_files:
    document = read_excel(READ_DIR + file)
    headers = list(document.keys())  # list of headers
    errors = 0
    for i in range(len(document)):
        try:
            values = ['']*len(headers)
            for j, header in enumerate(headers):
                if isna(document[header][i]):
                    values[j] = "NULL"
                elif j in [4]:
                    values[j] = d.get(document[header][i], document[header][i])
                elif j in [8, 14]:  # Date in format 31-JAN-19
                    some_date = datetime.datetime.strptime(document[header][i],
                                                           '%d-%b-%y')
                    values[j] = some_date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    raw = str(document[header][i])
                    modified = raw.replace("'", "''").strip(" ")
                    values[j] = modified

            insert_sql = (f"INSERT INTO X ("
                          f"{list_to_comma_seperated_values(headers)}"
                          f") VALUES ("
                          f"{list_to_comma_seperated_values(values)}"
                          f")\nGO\n")
            insert_sql_total += insert_sql
        except Exception:
            print("ISSUE with value")


if SEND:
    f = open("/cevac/cache/insert_work_orders.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_work_orders.sql")
    os.remove("/cevac/cache/insert_work_orders.sql")
if DEBUG:
    print(insert_sql_total)
    print(f"Last Excel Length: {len(document)}")
    print(f"Errors {errors}")

if SEND and not DEBUG:
    cleanup(PROCESSED_DIR)
