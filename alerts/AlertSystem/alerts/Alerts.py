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

from os import path
import datetime
import pyodbc
import pandas as pd
from tools import verbose_print

from .EventIDHandler import EventIDHandler
from .KnownIssues import KnownIssues
from .Parameters import Parameters
from .Occupancy import Occupancy
from .Anomaly import Anomaly

ENERGY_LOGS_LOCATION = "/mnt/bldg/Campus_Power/logs/"


class Alerts:
    """Handler for all alerts."""
    SKIP_STRING = None

    def __init__(
            self,
            logging : "logging",
            UPDATE_CACHE : bool,
            verbose=False,
            conn=None,
            queue=False,
            xref_only=True,
            debug=False
    ):
        """Initialize connection and other objects."""
        self.logging = logging
        self.UPDATE_CACHE = UPDATE_CACHE
        self.verbose = verbose
        self.debug = debug
        self.LOG = True
        if logging is None:
            self.LOG = False
        self.xref_only = xref_only
            
        self.conn = conn
        if conn is None:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=130.127.218.11;DATABASE=WFIC-CEVAC;'
                'UID=wficcm;PWD=5wattcevacmaint$'
            )
        self.occ = Occupancy(self.conn)
        self.par = Parameters(self.conn)  
        self.known_issues = KnownIssues(self.conn)
        self.eid_handler = EventIDHandler(
            self.conn, debug=debug, verbose=self.verbose
        )

        self.anomalies = []
        
        # For efficiency, only make each query once
        self.query_to_data = {}

        # Queue
        self.queue = queue
        self.queue_buildings = []
        self.remove_qids = set()
        if self.queue:
            self.queue_buildings = self.get_queue_buildings()

        self.sname_to_dname = self.get_sname_to_dname()

    def __call__(self) -> None:
        return self.alert_system()

    def alert_system(self) -> None:
        """Find and catalog all anomalies."""
        if self.LOG:
            logging.info(
                f"ALERT SYSTEM RUNNING"
            )

        # Check alerts for conditions
        for i, alert in enumerate(self.par.alert_parameters):
            # Check time conditional to make sure it is the correct
            # time for the alert
            if alert["aggregation"] == "LIVE":
                continue
            
            verbose_print(
                self.verbose,
                f"\nChecking Alert {i}: {alert}\n"
            )

            # Check basic value for basic alert
            if "numerical" in alert["type"]:
                metric = alert['metric']
                aggregation = alert['aggregation']
                buildings = self.par.metric_to_bldgs[metric]
                if "*" not in alert["building"]:
                    buildings = [alert["building"]]
                if self.queue:
                    buildings = self.queue_buildings_match(
                        buildings,
                        metric,
                        aggregation
                    )
                for building in buildings:
                    if self.skip_unoccupied(building, alert):
                        continue
                    table = f"CEVAC_{building}_{metric}_{aggregation}"
                    query = (f"SELECT * FROM {table}")
                    verbose_print(self.verbose, f"QUERY: {query}")
                    if not self.table_exists(table):
                        verbose_print(
                            self.verbose,
                            f"{table} does not exist"
                        )
                        continue
                    query += self.add_specific_aliases(alert)
                    data = self.safe_data(query)
                    for i in range(len(data)):
                        self.check_numerical_alias(
                            data, i, alert, building
                        )

            # Check each alias for relative temperature exceptions
            elif "temp" in alert["type"]:
                metric = alert['metric']
                aggregation = alert['aggregation']
                buildings = self.par.metric_to_bldgs[metric]
                if "*" not in alert["building"]:
                    buildings = [alert["building"]]
                if self.queue:
                    buildings = self.queue_buildings_match(
                        buildings,
                        metric,
                        aggregation
                    )
                for building in buildings:
                    if self.skip_unoccupied(building, alert):
                        continue
                    table = f"CEVAC_{building}_{metric}_{aggregation}"
                    query = (f"SELECT * FROM {table}")
                    verbose_print(self.verbose, f"QUERY: {query}")
                    if not self.table_exists(table):
                        verbose_print(
                            self.verbose,
                            f"{table} does not exist"
                        )
                        continue
                    query += self.add_specific_aliases(alert)
                    data = self.safe_data(query)
                    temps = {}
                    for i in range(len(data)):
                        alias = data["Alias"][i]
                        value = data["ActualValue"][i]

                        if not self.valid_temp_alias(alias):
                            continue

                        room = alias.split()[1]
                        if room in temps:
                            if "Temp" in alias:
                                temps[room]["Temp"] = value
                                temps[room]["name"] = alias
                            elif "Heating SP" in alias:
                                temps[room]["HeatingSP"] = value
                            elif "Cooling SP" in alias:
                                temps[room]["CoolingSP"] = value
                        else:
                            if "Temp" in alias:
                                temps[room] = {
                                    "Temp" : value,
                                    "name" : alias, 
                                }
                            elif "Heating SP" in alias:
                                temps[room] = {"HeatingSP" : value}
                            elif "Cooling SP" in alias:
                                temps[room] = {"CoolingSP": value}

                    for room in temps:
                        self.check_temp(temps, room, alert, building)

            # Check if aliases have reported within a given time
            elif "time" in alert["type"]:
                metric = alert['metric']
                aggregation = alert['aggregation']
                buildings = self.par.metric_to_bldgs[metric]
                if "*" not in alert["building"]:
                    buildings = [alert["building"]]
                if self.queue:
                    buildings = self.queue_buildings_match(
                        buildings,
                        metric,
                        aggregation
                    )
                for building in buildings:
                    if self.skip_unoccupied(building, alert):
                        continue
                    table = f"CEVAC_{building}_{metric}_{aggregation}"
                    if self.UPDATE_CACHE:
                        rebuild_broken_cache(table, self.conn)
                    query = (f"SELECT * FROM {table}_BROKEN_CACHE")
                    verbose_print(self.verbose, f"QUERY: {query}")
                    if not self.table_exists(table+"_BROKEN_CACHE"):
                        verbose_print(self.verbose, f"{table}_BROKEN_CACHE does not exist")
                        continue
                    query += self.add_specific_aliases(alert)
                    data = self.safe_data(query)
                    self.check_time(data, alert, building)

            elif "energy_num_buildings" in alert["type"]:
                if self.occ.is_occupied():
                    continue
                log_name = (
                    ENERGY_LOGS_LOCATION +
                    datetime.date.today().isoformat() +
                    ".log"
                )
                self.check_energy_num_buildings(log_name, alert)

        if self.LOG:
            logging.info(
                f"ALERT SYSTEM FINISHED"
            )
        if self.verbose:
            print(self.eid_handler)
        return None

    def send(self) -> None:
        """Send anomalies to sql."""

        # Add alerts for all clear
        for anomaly in self.anomalies:
            self.par.alerted_buildings[anomaly.building] = True
        for building in self.par.alerted_buildings:
            if self.par.alerted_buildings[building] == False:
                eventid = self.assign_event_id(
                    "All Clear", building, 0
                )
                self.anomalies.append(
                    Anomaly(
                        "All clear (No issues)",
                        "ALL",
                        building,
                        eventid,
                        0,
                        building,
                        "All Clear",
                        self.get_buildingdname(building),
                    )
                )
        
        self.erase_queue()
        
        # Write event IDs
        self.eid_handler.commit_removes()
        self.eid_handler.commit_adds()

        # Send each anomaly if it is not a known issue
        cursor = self.conn.cursor()
        for anomaly in self.anomalies:
            if anomaly.aliaspsid not in self.known_issues:
                anomaly.send(cursor)
        self.conn.commit()
        cursor.close()

        if self.LOG:
            self.logging.info(
                f"ANOMALIES SENT"
            )

    def safe_data(self, query : str) -> pd.DataFrame:
        """Return data if previously requested.
        
        Must check if table exists prior.
        """
        if query in self.query_to_data:
            return self.query_to_data[query]
        data = pd.read_sql_query(query, self.conn)
        self.query_to_data[query] = data
        return data

    def table_exists(self, table : str) -> bool:
        cursor = self.conn.cursor()
        if cursor.tables(table=table).fetchone():
            cursor.close()
            return True
        cursor.close()
        return False

    def replace_generic(
            self,
            message : str,
            alert : dict,
            context : dict
    ) -> str:
        """Return string with $ start at key replaced with 
        replacement.
        
        alert and context must have all keys be strings. 
        """
        
        # Add lower case to
        new_context = {}
        new_alert = {}
        for key in alert:
            new_alert[key.lower()] = str(alert[key])
        for key in context:
            new_context[key.lower()] = str(context[key])
        regex_list = message.split(" ")

        # Replace regexes
        for i, thing in enumerate(regex_list):
            if thing == "":
                continue
            if ((thing[0] in ["$", "@"]) or
                (thing.startswith("<") and thing.endswith(">"))):
                if thing[0] in ["$", "@"]:
                    replace = thing[1:].lower()
                else:
                    replace = thing[1:-1].lower()
                for key in new_alert:
                    if replace in key:
                        regex_list[i] = new_alert[key]
                for key in new_context:
                    if replace in key:
                        regex_list[i] = new_context[key]
                        
        return " ".join(regex_list)
                
    def skip_unoccupied(self, building : str, alert : dict) -> bool:
        """
        Return whether or not to skip the building based on 
        occupancy.
        """
        building_occupied = False
        if building in self.occ.building_occupied:
            building_occupied = self.occ.building_occupied[building]
        else:
            building_occupied = self.occ.building_occupied["*"]
        if "true" in alert["occupancy"].lower():
            if building_occupied:
                return False
            else:
                return True
        if "false" in alert["occupancy"].lower():
            if building_occupied:
                return True
            else:
                return False
        return False
        
    def assign_event_id(
            self,
            alert : dict,
            alias : str,
            psid : int
    ) -> int:
        """Assign event id."""
        return self.eid_handler.assign_event_id(alert, alias, psid)

    def get_alias_or_psid(self, table_name : str) -> str:
        """Return whether a table uses alias or point slice id."""
        request_str = (
            f"EXEC CEVAC_ALIAS_OR_PSID @table = '{table_name}'"
        )
        sol = pd.read_sql_query(request_str, self.conn)
        return sol[''][0]

    def get_psid_from_alias(
            self,
            alias : str,
            bldgsname : str,
            metric : str
    ) -> int:
        """Return the (most recent) pointsliceid from an alias."""
        SKIP = (self.SKIP_STRING, self.SKIP_STRING)
        xref = f"CEVAC_{bldgsname}_{metric}_XREF"
        pxref = f"CEVAC_{bldgsname}_{metric}_PXREF"
        if not self.xref_only:
            if self.table_exists(xref):
                data = self.safe_data(
                    f"SELECT px.PointSliceID, x.FLOOR "
                    f"FROM {pxref} as px "
                    f"FULL OUTER JOIN {xref} as x "
                    f"ON x.PointSliceID = px.PointSliceID"
                )
                return (
                    data["PointSliceID"][0], str(data["FLOOR"][0])
                )
            return SKIP
        else:
            if self.table_exists(xref):
                data = self.safe_data(
                    f"SELECT PointSliceID, Floor FROM {xref} "
                    f"WHERE ALIAS = '{alias}'"
                )
                if len(data) == 0:
                    return SKIP
                return (
                    data["PointSliceID"][0],
                    str(data["Floor"][0])
                )
            else:
                return SKIP


    def check_numerical_alias(
            self,
            data : pd.DataFrame,
            i : int,
            alert : dict,
            building : str
    ) -> None:
        """Check numerical alias alert."""
        conditions = alert["condition"].split(" ")
        
        actualvalue = "ActualValue"
        if actualvalue not in data.columns:
            if "Total_Usage" in data.columns:
                actualvalue = "Total_Usage"
            else:
                verbose_print(self.verbose, "NO VALID COLUMN")
                return None

        value = data[actualvalue][i]
        compare_value = 0
        for part in conditions:
            try:
                compare_value = float(part)
            except Exception:
                continue
        
        send_alert = False
        if ">" in conditions:
            send_alert = (value > compare_value)
        elif ">=" in conditiosn:
            send_alert = (value >= compare_value)
        elif "<" in conditions:
            send_alert = (value < compare_value)
        elif "<=" in conditions:
            send_alert = (value <= compare_value)
        elif "=" in conditions or "==" in conditions:
            send_alert = (value == compare_value)

        #input(data.columns)

        if "Alias" not in data:
            return None
        psid, floor = self.get_psid_from_alias(
            data["Alias"][i],
            building,
            alert["metric"]
        )
        if psid is self.SKIP_STRING or floor is self.SKIP_STRING:
            return None
        if send_alert:
            message = self.replace_generic(
                alert['message'],
                alert,
                {
                    "alias": f"{data['Alias'][i]} ({psid})",
                    "actualvalue": value,
                }
            )
            eventid = self.assign_event_id(
                alert, data["Alias"][i], psid
            )
            self.anomalies.append(
                Anomaly(
                    message,
                    alert["metric"],
                    building,
                    eventid,
                    f"{alert['priority']}",
                    f"{data['Alias'][i]} ({psid})",
                    alert["alert_name"],
                    self.get_buildingdname(building),
                    floor=str(floor),
                )
            )
        else:
            self.eid_handler.remove_event_id(
                data["Alias"][i],
                psid,
                alert,
            )
        return None

    def valid_temp_alias(self, alias : str) -> bool:
        """Return True if alias is valid for air temperatures."""
        valid = False
        if "RM" in alias:
            valid = True
        return valid

    def add_specific_aliases(
            self,
            alert : dict
    ) -> str:
        """Add where statement if applicable"""
        if "*" not in alert["aliaspsid"]:
            alias = alert["aliaspsid"].split(" ")
            new_alias = ""
            for a in alias:
                if "(" not in a:
                    new_alias += f"{a} "
            new_alias = new_alias.strip()
            return f" WHERE Alias = '{new_alias}'"
        return ""

    def check_temp(
            self,
            temps : dict,
            room : str,
            alert : dict,
            building : str
    ) -> None:
        """Check relative temperature values."""
        Alias_Temp = "Temp"
        if ("Temp" not in temps[room] or
            "CoolingSP" not in temps[room] or
            "HeatingSP" not in temps[room]):
            return None

        # Modify value
        room_vals = temps[room]
        val = 0
        if "+" in alert["condition"]:
            val_str = alert["condition"].split()[-1]
            val = float(val_str[val_str.find("+") + 1:])
            if "CoolingSP" in room_vals:
                room_vals["CoolingSP"] += val
            if "HeatingSP" in room_vals:
                room_vals["HeatingSP"] += val
        elif "-" in alert["condition"].split():
            val_str = alert["condition"].split()[-1]
            val = float(val_str[val_str.find("-") + 1:])
            if "CoolingSP" in room_vals:
                room_vals["CoolingSP"] -= val
            if "HeatingSP" in room_vals:
                room_vals["HeatingSP"] -= val

        # Check value
        send_alert = False

        if ">" in alert["condition"]:
            if "CoolingSP" in alert["condition"]:
                if "CoolingSP" in room_vals:
                    send_alert = (
                        room_vals["CoolingSP"] <
                        room_vals[Alias_Temp])
            if "HeatingSP" in alert["condition"]:
                if "HeatingSP" in room_vals:
                    send_alert = (
                        room_vals["HeatingSP"] <
                        room_vals[Alias_Temp])
        elif "<" in alert["condition"]:
            if "CoolingSP" in alert["condition"]:
                if "CoolingSP" in room_vals:
                    send_alert = (
                        room_vals["CoolingSP"] >
                        room_vals[Alias_Temp])
            if "HeatingSP" in alert["condition"]:
                if "HeatingSP" in room_vals:
                    send_alert = (
                        room_vals["HeatingSP"] >
                        room_vals[Alias_Temp])

        
        psid, floor = self.get_psid_from_alias(
            room_vals["name"], building, alert['metric']
        )
        if psid is self.SKIP_STRING or floor is self.SKIP_STRING:
            return None
        if send_alert:
            message = self.replace_generic(
                alert['message'],
                alert,
                {
                    "Alias": f"{room_vals['name']} ({psid})",
                    "ActualValue": "{0:.2f}".format(
                        room_vals["Temp"]
                    ),
                    "CoolingSP": "{0:.2f}".format(
                        room_vals["CoolingSP"]
                    ),
                    "HeatingSP": "{0:.2f}".format(
                        room_vals["HeatingSP"]
                    ),
                }
            )
            eventid = self.assign_event_id(
                alert, room_vals["name"], psid
            )
            self.anomalies.append(
                Anomaly(
                    message,
                    alert['metric'],
                    building,
                    eventid,
                    alert['priority'],
                    f"{room_vals['name']} ({psid})",
                    alert["alert_name"],
                    self.get_buildingdname(building),
                    floor=str(floor),
                )
            )
        else:
            self.eid_handler.remove_event_id(
                room_vals["name"],
                psid,
                alert
            )

        return None

    def check_time(
            self,
            data : pd.DataFrame,
            alert : dict,
            building : str
    ) -> None:
        """Check time off since last report."""
        for i in range(len(data)):
            #psid = data["PointSliceID"][i]
            psid, floor = self.get_psid_from_alias(
                data["Alias"][i], building, alert['metric']
            )
            if psid == None or floor == None:
                # We don't care about sensors with no xref
                continue
            now = datetime.datetime.utcnow()
            days_since = (now - data["UTCDateTime"][i]).days + 1
            message = self.replace_generic(
                alert['message'],
                alert,
                {
                    "Alias": f"{data['Alias'][i]} ({psid})",
                    "days": days_since,
                }
            )
            eventid = self.assign_event_id(
                alert, data["Alias"][i], psid
            )
            self.anomalies.append(
                Anomaly(
                    message,
                    alert['metric'],
                    building,
                    eventid,
                    alert['priority'],
                    f"{data['Alias'][i]} ({psid})",
                    alert["alert_name"],
                    self.get_buildingdname(building),
                )
            )
        return None

    def check_energy_num_buildings(
            self,
            log_name : str,
            alert : dict
    ) -> None:
        """Check number of successes in log file."""
        processed_file_neccessary = int(
            alert["condition"].split(" ")[-1]
        )
        num_processed_files = 0
        if path.isfile(log_name):
            log_file = open(log_name, "r")
            log_lines = log_file.readlines()
            for line in log_lines:
                if "INFO:Successfully imported data" in line:
                    num_processed_files += 1
        
        send_alert = False
        if "<" in alert["condition"]:
            if num_processed_files < processed_file_neccessary:
                send_alert = True
        if ">" in alert["condition"]:
            if num_processed_files > processed_file_neccessary:
                send_alert = True

        if send_alert:
            message = self.replace_generic(
                alert['message'],
                alert,
                {
                    "num_buildings": str(
                        processed_file_neccessary -
                        num_processed_files
                    ),
                }
            )
            eventid = self.assign_event_id(
                alert, alert["alert_name"], alert["alert_name"]
            )
            self.anomalies.append(
                Anomaly(
                    message,
                    alert['metric'],
                    "CAMPUS",
                    eventid,
                    alert['priority'],
                    f"N/A",
                    alert["alert_name"],
                    "CAMPUS"
                )
            )

        return None 

    def num_decom_anomalies(self) -> int:
        num = 0
        for anomaly in self.anomalies:
            if anomaly.aliaspsid in self.known_issues:
                num += 1
        return num

    def get_sname_to_dname(self) -> dict:
        """Get map of sname to dname."""
        data = pd.read_sql_query(
            "SELECT BuildingSName, BuildingDName "
            "FROM CEVAC_BUILDING_INFO",
            self.conn
        )
        a2b = {}
        for i in range(len(data)):
            a2b[data["BuildingSName"][i]] = data["BuildingDName"][i]
        return a2b

    def get_buildingdname(self, buildingsname : str) -> str:
        """Get building D name from building S name."""
        return self.sname_to_dname.get(buildingsname, buildingsname)

    def get_queue_buildings(self) -> pd.DataFrame:
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_ALERT_QUEUE",
            self.conn
        )
        return data

    def queue_buildings_match(
            self,
            buildings : list,
            metric : str,
            age : int
    ) -> list:
        """
        Returns list of buildings that should be checked and
        are in the queue.
        """
        qb = []
        print(self.queue_buildings)
        for i in range(len(self.queue_buildings)):
            if (
                    self.queue_buildings["Age"][i] == age and
                    self.queue_buildings["Metric"][i] == metric
            ):
                qb.append(self.queue_buildings["BuildingSName"][i])
                self.remove_qids.add(self.queue_buildings["QID"][i])
        print(f"QB {qb}")
        matching_buildings = list(
            set(qb) & set(buildings)
        )
        print(f"Matching Queue Buildings {matching_buildings}")
        return matching_buildings

    def erase_queue(self) -> None:
        if not self.queue:
            return None
        cursor = self.conn.cursor()
        for QID in self.remove_qids:
            cursor.execute(
                f"DELETE FROM CEVAC_ALERT_QUEUE "
                f"WHERE QID = {QID}"
            )
        cursor.commit()
        cursor.close()
        return None

# For debugging
if __name__ == "__main__":
    print("DEBUG ALERT SYSTEM")
    
    all_alerts = Alerts(None, False, verbose=True)
    
    print(f"OCCUPIED BUILDINGS: {all_alerts.occ.building_occupied}\n")
    print(f"ALERT PARAMETERS: {all_alerts.par.alert_parameters}\n")
    print(f"METRIC TO BLDGS: {all_alerts.par.metric_to_bldgs}\n")
    print(f"DECOMMISSIONED: {all_alerts.known_issues.alias_psid}\n")
    print(f"MAX EVENT ID: {all_alerts.max_id}")
    print(f"LATEST EVENTS: {all_alerts.old_events}")
    print(f"SNAME TO DNAME: {all_alerts.sname_to_dname}")
    
    input("PAUSE -- PRESS ENTER TO RUN ALERT SYSTEM -- PAUSE")
    
    all_alerts.alert_system()

    for a in all_alerts.anomalies:
        if a.aliaspsid in all_alerts.known_issues:
            continue
        print(str(a))
    print(
        f"\n\n{len(all_alerts.anomalies)} anomalies"
        f"\n{all_alerts.num_decom_anomalies()} decommissioned"
    )
    
    do_commit = input("Commit to DB? ").lower()
    
    if "y" in do_commit and "n" not in do_commit:
        all_alerts.send()

    all_alerts.conn.close()
        
    print("FINISHED")


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
