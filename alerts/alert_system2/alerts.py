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

ENERGY_LOGS_LOCATION = "/mnt/bldg/Campus_Power/logs/"


class Alerts:
    """Handler for all alerts."""

    def __init__(self, logging, UPDATE_CACHE, verbose=False,
                 conn=None):
        """Initialize connection and other objects."""
        self.logging = logging
        self.UPDATE_CACHE = UPDATE_CACHE
        self.LOG = True
        if logging is None:
            self.LOG = False
            
        self.conn = conn
        if conn is None:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=130.127.218.11;DATABASE=WFIC-CEVAC;'
                'UID=wficcm;PWD=5wattcevacmaint$'
            )
        self.occ = Occupancy(self.conn)
        self.par = Parameters(self.conn)  
        self.known_issues = Known_Issues(self.conn)

        self.verbose = verbose
        self.anomalies = []
        
        # For efficiency, only make each query once
        self.query_to_data = {}
        
        self.json_oc = "/cevac/cron/alert_log_oc.json"
        self.json_unoc = "/cevac/cron/alert_log_unoc.json"
        self.json_files = [
            self.json_oc,
            self.json_unoc,
        ]
        self.max_id = 0
        self.new_events = {}
        self.old_events = {}
        self.parse_json()

        self.sname_to_dname = self.get_sname_to_dname()

    def alert_system(self):
        """Find and catalog all anomalies."""
        if self.LOG:
            logging.info(
                f"ALERT SYSTEM RUNNING"
            )

        # Check alerts for conditions
        for i, alert in enumerate(self.par.alert_parameters):
            # Check time conditional to make sure it is the correct
            # time for the alert
            
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
                for building in buildings:
                    if self.skip_unoccupied(building, alert):
                        continue
                    table = f"CEVAC_{building}_{metric}_{aggregation}"
                    if self.UPDATE_CACHE:
                        rebuild_broken_cache(table, self.conn)
                    query = (f"SELECT * FROM {table}_BROKEN_CACHE")
                    verbose_print(self.verbose, f"QUERY: {query}_BROKEN_CACHE")
                    if not self.table_exists(table+"_BROKEN_CACHE"):
                        verbose_print(self.verbose, f"{table}_BROKEN_CACHE does not exist")
                        continue
                    query += self.add_specific_aliases(alert)
                    data = self.safe_data(query)
                    self.check_time(data, alert, building)

            elif "energy_num_buildings" in alert["type"]:
                log_name = (
                    ENERGY_LOGS_LOCATION +
                    datetime.date.today().isoformat() +
                    ".log"
                )
                self.check_energy_num_buildings(log_name, alert)

            # TODO all clear
        insert_sql_total = (
            f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType,"
            f"AlertMessage,Metric,UTCDateTime,MessageID) "
            f"VALUES('All Clear','All Clear','N/A',"
            f"GETUTCDATE(),'0')"
        )
        if self.LOG:
            logging.info(
                f"ALERT SYSTEM FINISHED"
            )


    def send(self):
        """Send anomalies to sql."""
        
        # Write event IDs
        self.write_json_generic(self.new_events, self.max_id)  

        # Send each anomaly if it is not a known issue
        cursor = self.conn.cursor()
        for anomaly in self.anomalies:
            if anomaly.aliaspsid not in self.known_issues.alias_psid:
                anomaly.send(cursor)
        self.conn.commit()
        cursor.close()

        if self.LOG:
            self.logging.info(
                f"ANOMALIES SENT"
            )
            self.logging.shutdown()

    def safe_data(self, query):
        """Return data if prevviously requested.
        
        Must check if table exists prior.
        """
        if query in self.query_to_data:
            return self.query_to_data
        return pd.read_sql_query(query, self.conn)

    def table_exists(self, table):
        cursor = self.conn.cursor()
        if cursor.tables(table=table).fetchone():
            cursor.close()
            return True
        cursor.close()
        return False

    def write_json_generic(self, new_events, next_id):
        """Write json independent of time."""
        new_events["next_id"] = next_id
        if self.occ.is_occupied():
            f = open(self.json_oc, "w")
        else:
            f = open(self.json_unoc, "w")
        f.write(json.dumps(new_events))
        f.close()
        return None

    def parse_json(self):
        """Parse json(s) for cron use."""
        new_json = {}
        for filename in self.json_files:
            f = open(filename, "r")
            line = f.readlines()[0]
            new_json.update(json.loads(line))
            nid = new_json["next_id"]
            self.max_id = max(nid, self.max_id)
            f.close()
        self.old_events = new_json
        return None

    def replace_generic(self, message, alert, context):
        """Return string with $ start at key replaced with replacement.
        
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
                
    def skip_unoccupied(self, building, alert):
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
        
    def assign_event_id(self, alert, alias, psid):
        """Assign event id."""
        key = f"{alias} {psid} {alert['type']}"
        event_id = self.max_id
        if key in self.old_events:
            event_id = self.old_events[key]
            self.new_events[key] = event_id
        else:
            self.max_id += 1
            self.new_events[key] = event_id
        return event_id

    def get_alias_or_psid(self, table_name):
        """Return whether a table uses alias or point slice id."""
        request_str = (
            f"EXEC CEVAC_ALIAS_OR_PSID @table = '{table_name}'"
        )
        sol = pd.read_sql_query(request_str, self.conn)
        return sol[''][0]

    def get_psid_from_alias(self, alias, bldgsname, metric):
        """Return the (most recent) pointsliceid from an alias."""
        xref = f"CEVAC_{bldgsname}_{metric}_XREF"
        if self.table_exists(xref):
            data = pd.read_sql_query(
                f"SELECT PointSliceID, Floor FROM {xref} "
                f"WHERE ALIAS = '{alias}'",
                self.conn
            )
            return (data["PointSliceID"][0], data["Floor"][0])
        return "?", ""

    def check_numerical_alias(self, data, i, alert, building):
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

        if send_alert:
            psid, floor = self.get_psid_from_alias(
                data["Alias"][i],
                building,
                alert["metric"]
            )
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
        return None

    def valid_temp_alias(self, alias):
        """Return True if alias is valid for air temperatures."""
        valid = False
        if "RM" in alias:
            valid = True
        return valid

    def add_specific_aliases(self, alert):
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

    def check_temp(self, temps, room, alert, building):
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

        if send_alert:
            psid, floor = self.get_psid_from_alias(
                room_vals["name"], building, alert['metric']
            )
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

        return None

    def check_time(self, data, alert, building):
        """Check time off since last report."""
        for i in range(len(data)):
            psid = data["PointSliceID"][i]
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

    def check_energy_num_buildings(self, log_name, alert):
        """Check number of successes in log file."""
        processed_file_neccessary = int(
            alert["condition"].split(" ")[-1]
        )
        num_processed_files = 0
        if os.path.isfile(log_name):
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
        

    def num_decom_anomalies(self):
        num = 0
        for anomaly in self.anomalies:
            if anomaly.aliaspsid in self.known_issues.alias_psid:
                num += 1
        return num

    def get_sname_to_dname(self):
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

    def get_buildingdname(self, buildingsname):
        """Get building D name from building S name."""
        return self.sname_to_dname.get(buildingsname, buildingsname)

    def __del__(self):
        """Deconstructor."""
        self.conn.close()


class Anomaly:
    def __init__(self, message, metric, building, eventid,
                 priority, aliaspsid, alert_name, buildingdname,
                 floor=""):
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
        self.floor = floor

    def send(self, cursor):
        stat = (
            f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW "
            f"(AlertType, AlertMessage, Metric, BuildingSName, "
            f"UTCDateTime, Alias, EventID, BuildingDName) VALUES "
            f"(?, ?, ?, ?, ?, ?, ?, ?);"
        )
        cursor.execute(stat, [
            self.priority,
            self.message,
            self.metric,
            self.building,
            self.time,
            self.aliaspsid,
            self.eventid,
            self.buildingdname,
        ])
        cursor.commit()
        
        return None

    def __str__(self):
        sstr = (
            f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW"
            f"(AlertType, AlertMessage, Metric, BuildingSName, "
            f"UTCDateTime, Alias, EventID, BuildingDName) "
            f"VALUES('{self.priority}', '{self.message}', "
            f"'{self.metric}', "
            f"'{self.building}', '{self.time}', '{self.aliaspsid}', "
            f"'{self.eventid}', '{self.buildingdname}')"
        )
        return sstr


class Occupancy:
    """Simple singleton to maintain occupancy data."""

    def __init__(self, conn):
        """Initialize building_occupied map."""
        data = pd.read_sql_query("SELECT * FROM CEVAC_OCCUPANCY", conn)
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
                        self.building_occupied[item] = data[occstr][i]
                    self.building_occupied["*"] = data[occstr][i]
                else:
                    self.building_occupied[
                        data[bsn][i]] = data[occstr][i]

    def building_is_occupied(self, building):
        """Return True if in occupied time."""
        if building not in self.building_occupied:
            return self.building_occupied["*"]
        else:
            return self.building_occupied[building]

    def is_occupied(self):
        """Return True if in occupied time."""
        now = datetime.datetime.now()
        day = now.isoweekday()
        hour = now.hour
        correct_day = (day >= 1 and day <= 5)
        correct_hour = (hour >= 8 and hour < 17)
        if (correct_day and correct_hour):
            return True
        return False

    def cron_is_now(self, cron, offset=5):
        """Return True if cron is within 5 minutes of now."""
        now = datetime.datetime.utcnow()
        c = croniter(cron)
        td = (now - c.get_next(datetime.datetime))
        td_min = abs(td.total_seconds()/60)
        if td_min < offset:
            return True
        return False


class Parameters:
    """Represents alert parameters."""
    
    def __init__(self, conn):
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
        self.metric_to_bldgs = self.get_active_buildings(conn)

    def type_from_condition(self, condition):
        if "time" in condition.lower():
            return "time"
        if "coolingsp" in condition.lower():
            return "temp"
        if "heatingsp" in condition.lower():
            return "temp"
        if "energy_num_buildings" in condition.lower():
            return "energy_num_buildings"
        return "numerical"

    def get_aliases(self, parameter):
        if "*" in parameter["aliaspsid"]:
            return ["*"]

    def get_active_buildings(self, conn):
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
            if metric in metric_to_bldgs:
                metric_to_bldgs[metric].append(bldg)
            else:
                metric_to_bldgs[metric] = [bldg]
        return metric_to_bldgs

class Known_Issues:
    """Represents known issues to ignore."""
    
    def __init__(self, conn):
        """Initialize known issues."""
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_KNOWN_ISSUES",
            conn
        )
        self.alias_psid = {}
        for i in range(len(data)):
            if 'decomissioned' in data['Code'][i].lower():
                self.alias_psid[data['PSID_Alias'][i]] = None

    def check_aliaspsid(self, aliaspsid):
        return (aliaspsid in self.alias_psid)


def rebuild_broken_cache(table, conn):
    """Rebuild a broken cache."""
    cursor = conn.cursor()
    cursor.execute("EXEC CEVAC_CACHE_INIT @tables = '{table}_BROKEN'")
    cursor.commit()
    conn.commit()
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
        if a.aliaspsid in all_alerts.known_issues.alias_psid:
            continue
        print(str(a))
    print(
        f"\n\n{len(all_alerts.anomalies)} anomalies"
        f"\n{all_alerts.num_decom_anomalies()} decommissioned"
    )
    
    do_commit = input("Commit to DB? ").lower()
    
    if "y" in do_commit and "n" not in do_commit:
        all_alerts.send()
        
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
