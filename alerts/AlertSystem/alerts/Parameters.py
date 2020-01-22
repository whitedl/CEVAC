"""
Iterable alert parameter handler.
"""

import pyodbc
import pandas as pd
from tools import verbose_print


class Parameters:
    """Represents alert parameters."""
    
    def __init__(self, conn : pyodbc.Connection):
        """Initialize parameters."""
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_ALERT_PARAMETERS",
            conn
        )
        self.alert_parameters = []
        for i in range(len(data)):
            self.alert_parameters.append({
                "alert_name": data['alert_name'][i],
                "metric": data['Metric'][i],
                "condition": data['Condition'][i],
                "message": data['message'][i],
                "occupancy": data['occupancy'][i],
                "building": data['BuildingSName'][i],
                "aggregation": data['aggregation'][i],
                "priority": data['Priority'][i],
                "aliaspsid": data["Alias_PSID"][i],
                "type": self.type_from_condition(
                    data['Condition'][i]
                ),
            })
        self.alerted_buildings = {}
        self.metric_to_bldgs = self.get_active_buildings(conn)

    def type_from_condition(self, condition : str) -> str:
        if "time" in condition.lower():
            return "time"
        if "coolingsp" in condition.lower():
            return "temp"
        if "heatingsp" in condition.lower():
            return "temp"
        if "energy_num_buildings" in condition.lower():
            return "energy_num_buildings"
        return "numerical"

    def get_active_buildings(
            self,
            conn : pyodbc.Connection
    ) -> dict:
        data = pd.read_sql_query(
            "SELECT DISTINCT BUILDINGSNAME, METRIC "
            "FROM CEVAC_TABLES WHERE TABLENAME "
            "LIKE '%HIST_VIEW%'",
            conn
        )
        metric_to_bldgs = {}
        for i in range(len(data)):
            metric = data["METRIC"][i]
            bldg = data["BUILDINGSNAME"][i]
            self.alerted_buildings[bldg] = False
            if metric in metric_to_bldgs:
                metric_to_bldgs[metric].append(bldg)
            else:
                metric_to_bldgs[metric] = [bldg]
        return metric_to_bldgs

    def __str__(self) -> str:
        return (
            f"PARAMETERS ({self.alert_parameters})"
        )

    def __repr__(self) -> str:
        return (
            f"PARAMETERS #({len(self)})"
        )

    def __len__(self) -> int:
        return len(self.alert_parameters)

    def __getitem__(self, position : int) -> dict:
        key = list(self.alert_parameters.keys())[position]
        return self.alert_parameters[key]

    def __contains__(self, item : dict) -> bool:
        return (item in self.alert_parameters)

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
