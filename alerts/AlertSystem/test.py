"""
Tools for testing alert sytem.

If something breaks, find the line number and
read the corresponding comment to debug.

This should check both that logic and syntax 
is valid.
"""

import unittest
import pyodbc
import pandas as pd
import datetime

from alerts.Occupancy import Occupancy
from alerts.EventIDHandler import EventIDHandler
from alerts.KnownIssues import KnownIssues
from alerts.Parameters import Parameters
from alerts.Anomaly import Anomaly


class TestOccupancy(unittest.TestCase):

    def test_length(self):
        occ = Occupancy(conn)
        self.assertTrue(len(occ) > 1)
        # If error, means occupancy table
        # isn't being read correctly, it should
        # have more information

    def test_current_occupancy(self):
        occ = Occupancy(conn)
        hour = datetime.datetime.now().hour
        if hour > 8 and hour < 17:
            self.assertTrue(occ.is_occupied())
        else:
            self.assertFalse(occ.is_occupied())
        # If error, means croniter parsing is
        # broken
        


class TestEventIDHandler(unittest.TestCase):

    def test_lengths(self):
        eidh = EventIDHandler(conn)
        self.assertTrue(len(eidh) == 0)
        self.assertTrue(eidh.new_ids == 0)
        self.assertTrue(eidh.old_ids == 0)
        self.assertFalse(eidh)
        # If error, means EventIDHandler
        # is erroring new and old ids

    def test_next_id(self):
        eidh = EventIDHandler(conn)
        self.assertTrue(eidh.next_id > 2)
        # If error, means max_id (or next id)
        # for events is broken


class TestKnownIssues(unittest.TestCase):

    def test_length(self):
        ki = KnownIssues(conn)
        self.assertTrue(ki)
        self.assertTrue(len(ki) > 5)
        # If error, known issues is not
        # read correctly

    def test_specific_aliaspsids(self):
        ki = KnownIssues(conn)
        aliaspsids = [
            "RM 344A / Heating SP (8880)",
            "Air Handler R1 Return Air 3rd Floor CO2 (6640)"
        ]
        for ap in aliaspsids:
            self.assertTrue(ap in ki)
        # If error, known issues table has
        # been corrupted


class TestParameters(unittest.TestCase):

    def test_length(self):
        par = Parameters(conn)
        self.assertTrue(len(par) > 8)
        # if error, parameters table has
        # been corrupted, or data didn't
        # pull correctly

    def test_active_buildings(self):
        par = Parameters(conn)
        self.assertTrue(
            len(par.get_active_buildings(conn)) > 5
        )
        # If error, CEVAC_TABLES may be broken


class TestAnomaly(unittest.TestCase):

    def test_anomaly_creation(self):
        a1 = Anomaly(
            "TEST TEMP",
            "TEMP",
            "WATT",
            419,
            2,
            "SOME SENSOR (68)",
            "TEST",
            "WFIC",
            floor=4
        )
        self.assertTrue(a1)
        a2 = Anomaly(
            "TEST TEMP",
            "TEMP",
            "WATT",
            -1,
            2,
            "SOME SENSOR (68)",
            "TEST",
            "WFIC",
            floor=4
        )
        self.assertFalse(a2)
        # If error, eventIDs are broken

    def test_equality(self):
        a1 = Anomaly(
            "TEST CO2",
            "CO2",
            "WATT",
            33,
            2,
            "SOME SENSOR (68)",
            "TEST",
            "WFIC",
            floor=4
        )
        a2 = Anomaly(
            "TEST WAP",
            "DOESN'T MATTER",
            "WATT",
            33,
            2,
            "SOME SENSOR (68)",
            "TEST",
            "WFIC",
            floor=68
        )
        self.assertTrue(a1 == a2)
        # If error, equality is broken

        
if __name__ == "__main__":
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=130.127.218.11;"
        "DATABASE=WFIC-CEVAC;"
        "UID=wficcm;"
        "PWD=5wattcevacmaint$"
    )
    unittest.main()
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
