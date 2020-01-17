"""
Represents a detected issue. 
"""

import os
import json
import datetime
import pytz
import logging
from copy import deepcopy
from croniter import croniter
import pyodbc
import pandas as pd
import sys
from tools import verbose_print


class Anomaly:
    def __init__(
            self,
            message : str,
            metric : str,
            building : str,
            eventid : int,
            priority : int,
            aliaspsid : str,
            alert_name : str,
            buildingdname : str,
            floor=""
    ):
        self.message = message
        self.metric = metric
        self.building = building
        self.eventid = int(eventid)
        self.priority = str(priority)
        self.aliaspsid = aliaspsid
        self.time = datetime.datetime.utcnow()
        self.alert_name = alert_name
        self.buildingdname = buildingdname

        # Optional, not always available
        self.floor = str(floor)

        self.original = True

    def send(self, cursor : pyodbc.Connection) -> str:
        stat = (
            f"IF EXISTS(SELECT TOP 1 EventID FROM "
            f"CEVAC_ALL_ALERTS_EVENTS_HIST_RAW WHERE "
            f"EventID = {self.eventid}) BEGIN "
            f"UPDATE CEVAC_ALL_ALERTS_EVENTS_HIST_RAW "
            f"SET AlertMessage = '{self.message}', "
            f"latest_UTC = GETUTCDATE(), "
            f"AlertType = '{self.priority}'"
            f"WHERE EventID = {self.eventid}; "
            f"END ELSE BEGIN "
            f"INSERT INTO CEVAC_ALL_ALERTS_EVENTS_HIST_RAW "
            f"(EventID, AlertType, AlertMessage, BuildingSName, "
            f"Metric, latest_UTC) "
            f"VALUES (?, ?, ?, ?, ?, GETUTCDATE()); END"
        )
        
        cursor.execute(stat, [
            self.eventid,
            self.priority,
            self.message,
            self.building,
            self.metric
        ])
        cursor.commit()
        
        return None

    def __str__(self) -> str:
        return (
            f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW"
            f"(AlertType, AlertMessage, Metric, BuildingSName, "
            f"UTCDateTime, Alias, EventID) "
            f"VALUES('{self.priority}', '{self.message}', "
            f"'{self.metric}', "
            f"'{self.building}', '{self.time}', "
            f"'{self.aliaspsid}', "
            f"'{self.eventid}')"
        )

    def __repr__(self) -> str:
        return (
            f"ANOMALY: {self.metric} {self.building} "
            f"{self.aliaspsid} "
            f"- EVENTID {self.eventid}"
        )

    def __len__(self) -> int:
        return 1

    def __eq__(self, other : "Anomaly") -> bool:
        if self.eventid == other.eventid:
            return True
        return False

    def __nonzero__(self) -> bool:
        if self.eventid > 1:
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
