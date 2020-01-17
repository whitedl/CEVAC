"""
itest.py
Tools for integration testing the alert sytem.

If something breaks, find the line number and
read the corresponding comment to debug.

This should check both that logic and syntax 
is valid.
"""

import pyodbc
import pandas as pd
import datetime

from alerts.Occupancy import Occupancy
from alerts.EventIDHandler import EventIDHandler
from alerts.KnownIssues import KnownIssues
from alerts.Parameters import Parameters
from alerts.Anomaly import Anomaly
from alerts.Alerts import Alerts


class TestAlertSystem:

    def __call__(self):
        print(self.test_whole_system())
    
    def test_whole_system(self):
        a = Alerts(None, conn)
        a()
        


if __name__ == "__main__":
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=130.127.218.11;"
        "DATABASE=WFIC-CEVAC;"
        "UID=wficcm;"
        "PWD=5wattcevacmaint$"
    )
    AS = TestAlertSystem()
    AS()
    conn.close()

"""
      /##.*/
     /#%&&%#/
    ./%%%&%%#
    %%%%&%&%%#
   %&&  %%%&%%.
   %&%  &%%&%%*
   *%&@&@%&%%(
     %%%%%%%%
"""
