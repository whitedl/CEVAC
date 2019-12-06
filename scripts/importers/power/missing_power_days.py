"""
Find missing power days.
"""

import pyodbc
import pandas as pd
import datetime


if __name__ == "__main__":
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=130.127.218.11;"
        "DATABASE=WFIC-CEVAC;"
        "UID=wficcm;"
        "PWD=5wattcevacmaint$"
    )

    bldg = input("BuildingSName: ").upper()

    data = pd.read_sql_query(
        (f"SELECT * FROM CEVAC_CAMPUS_ENERGY_HIST "
         f"WHERE Alias LIKE '%{bldg}%' "
         f"AND hour_offset >= 24 "
         f"ORDER BY ETDateTime DESC"),
        conn
    )

    # Find days originally missing
    days_missing = []
    for i in range(len(data)):
        hours_off = data["hour_offset"][i]
        dt = data["ETDateTime"][i]
        while hours_off > 0:
            dt -= datetime.timedelta(days=1)
            days_missing.append(dt)
            hours_off -= 24

    # Check that days are still missing
    still_missing = [True for day in days_missing]
    for i, day in enumerate(days_missing):
        data = pd.read_sql_query(
            (f"SELECT TOP 1 * FROM CEVAC_CAMPUS_ENERGY_HIST "
             f"WHERE Alias LIKE '%{bldg}%'"
             f"AND ETDateTime = '{str(day)}'"),
            conn
        )
        if len(data) == 0:
            still_missing[i] = True
        else:
            still_missing[i] = False

    for day, missing in zip(days_missing, still_missing):
        if missing:
            print(day.strftime("%m-%d-%Y"),end=", ")

    
