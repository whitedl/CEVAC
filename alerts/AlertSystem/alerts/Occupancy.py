"""CEVAC alert managment, object oriented.

This CEVAC alert system script populates the table 
`CEVAC_ALL_ALERTS_HIST` with data anomalies.

Anomalies are determined by comparing recent data from tables 
defined by the table `CEVAC_ALERT_PARAMETERS`. Anomalies are
stored in the table `CEVAC_ALL_ALERTS_HIST_RAW`. Anomalies are 
grouped by the EventID in order to remove the storage of
multiple anomalies in the events table. Anomalies that are
known and accounted for (but still occur for whatever reason)
are cited as a known issue and are located in 
`CEVAC_KNOWN_ISSUES`.
"""

import datetime
import pytz
from croniter import croniter
import pyodbc
import pandas as pd
from tools import verbose_print

class Occupancy:
    """Simple singleton to maintain occupancy data."""

    def __init__(self, conn : pyodbc.Connection):
        """Initialize building_occupied map."""
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_OCCUPANCY",
            conn
        )
        
        self.building_occupied = {"*": False}
        for i in range(len(data)):
            crontab = (f"{data['Minutes'][i]} {data['Hour'][i]} "
                       f"{data['Day_month'][i]} "
                       f"{data['Month'][i]} {data['Day_week'][i]}")
            bsn = "BuildingSName"
            occstr = "Occupied"
            if data['Cron_Occupancy'][i]:
                if not self.cron_is_now(crontab):
                    continue
                if "*" in data[bsn][i]:
                    for item in self.building_occupied:
                        self.building_occupied[item] = (
                            data[occstr][i]
                        )
                    self.building_occupied["*"] = data[occstr][i]
                else:
                    self.building_occupied[
                        data[bsn][i]] = data[occstr][i]

    def building_is_occupied(self, building : str) -> bool:
        """Return True if in occupied time."""
        if building not in self.building_occupied:
            return self.building_occupied["*"]
        else:
            return self.building_occupied[building]

    def is_occupied(self) -> bool:
        """Return True if in occupied time."""
        now = datetime.datetime.now()
        day = now.isoweekday()
        hour = now.hour
        correct_day = (day >= 1 and day <= 5)
        correct_hour = (hour >= 8 and hour < 17)
        if (correct_day and correct_hour):
            return True
        return False

    def cron_is_now(self, cron : str, offset=5) -> bool:
        """Return True if cron is within 5 minutes of now."""
        now = datetime.datetime.utcnow()
        c = croniter(cron)
        td = (now - c.get_next(datetime.datetime))
        td_min = abs(td.total_seconds()/60)
        if td_min < offset:
            return True
        return False

    def __str__(self) -> str:
        return (
            f"OCCUPANCY {self.building_occupied}"
        )

    def __repr__(self) -> str:
        return (
            f"OCCUPANCY #({len(self.building_occupied) - 1})"
        )

    def __len__(self) -> int:
        if len(self.building_occupied) > 1:
            return len(self.building_occupied)
        return 0

    def __contains__(self, item : str) -> bool:
        if item in self.building_occupied:
            return True
        return False

    def __nonzero__(self) -> bool:
        if len(self) > 0:
            return True
        return False

    def __bool__(self) -> bool:
        return self.__nonzero__()

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
