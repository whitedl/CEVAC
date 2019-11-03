"""CEVAC alert managment, object oriented.

This CEVAC alert system script populates the table `CEVAC_ALL_ALERTS_HIST`.
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


# JSON files
json_oc = "/cevac/cron/alert_log_oc.json"
json_unoc = "/cevac/cron/alert_log_unoc.json"

# Time constants
TIME = {
    "day": 1,
    "hr": 24,
    "hour": 24,
    "min": 24 * 60,
    "minute": 24 * 60,
    "minutes": 24 * 60,
}


class Alerts:
    """Handler for all alerts."""

    def __init__(self, logging, verbose=False):
        """Initialize connection and other objects."""
        self.logging = logging
        self.LOG = True
        if logging is None:
            self.LOG = False
            
        self.conn = pyodbc.connect('DRIVER='
                                   '{ODBC Driver 17 for SQL Server};'
                                   'SERVER=130.127.218.11;'
                                   'DATABASE=WFIC-CEVAC;'
                                   'UID=wficcm;PWD=5wattcevacmaint$')
        self.occ = Occupancy(self.conn)
        #self.par = Parameters(self.conn)
        #self.known_issues = Known_Issues(self.conn)
        self.verbose = verbose
        self.anomalies = []

    def alert_system(self):
        """Find and catalog all anomalies."""

        # Parse json files for event IDs
        self.parse_json(json_oc, json_unoc)
        
        # Go through each alert parameter
        for i, alert in enumerate(self.par.alert_parameters):
            if alert.aliaspsid is "":
                pass  # TODO
            else:
                for building in self.building_s_list():
                    if self.skip_building(building, alert):
                        continue
                    
                    if "@actualvalue" in alert.condition.lower():
                        self.check_numerical(alert, building)
                    elif "@temp" in alert.condition.lower():
                        self.check_temp(alert, building)
                    elif "@time" in alert.condition.lower():
                        self.check_time(alert, building)
                    else:
                        self.safe_log("Could not find valid "
                                      f"condition/value for {alert}",
                                      "error")
                        print(f"ERROR: Invalid condition on row {i+1}")

    def send(self):
        """Send anomalies to sql."""
        self.write_json_generic(new_events, next_id)  # Write event IDs

        # Commit db changes TODO

        if self.LOG:
            self.logging.info(str(datetime.datetime.now()))
            self.logging.shutdown()

    def write_json_generic(self, new_events, next_id):
        """Write json independent of time."""
        new_events["next_id"] = next_id
        if self.occ.is_occupied():
            f = open(json_oc, "w")
        else:
            f = open(json_unoc, "w")
        f.write(json.dumps(new_events))
        f.close()
        return None

    def parse_json(self, *filenames):
        """Parse json(s) for cron use."""
        self.next_id = 0
        self.old_json = {}
        for filename in filenames:
            try:
                f = open(filename, "r")
                line = f.readlines()[0]
                self.old_json.update(json.loads(line))
                nid = new_json["next_id"]
                self.next_id = max(nid, self.next_id)
                f.close()
            except Exception:
                continue
        return None

    def angle_brackets_replace_specific(self, regex_string, key, replacement):
        """Return string with angle brackets at key replaced with replacement."""
        try:
            regex_list = regex_string.split(f"<{key}>")
            for i, regex in enumerate(regex_list):
                if i < len(regex_list) - 1:
                    regex_list[i] += str(replacement)
            return "".join(regex_list)
        except Exception:
            return regex_string

    def skip_alias(self, known_issues, bldg, alias, metric):
        """Check known issues for decomissioned alias."""
        psid = get_psid_from_alias(alias, bldg, metric)
        if bldg not in known_issues:
            return False
        for message in known_issues[bldg]:
            if f"({psid})" in message:
                return True
        return False

    def assign_event_id(self, alert, alias):
        """Assign event id."""
        key = alias + alert.message_id
        event_id = self.next_id
        if key in self.old_json:
            event_id = self.old_json[key]
            self.new_json[key] = event_id
        else:
            self.next_id += 1
            self.new_json[key] = event_id
        
        return event_id

    def get_alias_or_psid(self, table_name):
        """Return whether a table uses alias or point slice id."""
        request_str = f"EXEC CEVAC_ALIAS_OR_PSID @table = '{table_name}'"
        sol = pd.read_sql_query(request_str, self.conn)
        return sol[''][0]

    def get_psid_from_alias(self, alias, bldgsname, metric):
        """Return the (most recent) pointsliceid from an alias."""

        # TODO doesn't work
        print(f"Get psid from alias: {alias} {bldgsname} {metric}")
        command = (f"EXEC CEVAC_XREF_LOOKUP @BuildingSName = '{bldgsname}', "
                   f"@Metric = '{metric}', @Alias = '{alias}'")
        sol = pd.read_sql_query(command, self.conn)
        psids = []
        return str(max(psids))

    def get_alias_from_psid(self, psid, bldgsname, metric):
        """Return the (most recent) pointsliceid from an alias."""

        # TODO doesnt' work
        print(f"Get psid from alias: {alias} {bldgsname} {metric}")
        command = (f"EXEC CEVAC_XREF_LOOKUP @BuildingSName = '{bldgsname}', "
                   f"@Metric = '{metric}', @PointSliceID = {psid}")
        sol = pd.read_sql_query(command, self.conn)
        psids = []
        return str(max(psids))


    def check_numerical(self, alert, building):
        """Check numerical alias alert."""
        selection_command = (f"SELECT * FROM "
                             f"CEVAC_{alert.metric}_"
                             f"{alert.bldg_s_name}_"
                             f"{aggregation}")

        data = pd.read_sql_query(selection_command, self.conn)
        id_column = "Alias" if "Alias" in data.columns else "PointSliceID"

        for i in range(len(data)):
            value = data["ActualValue"][i]
            compare_value = float(alert.condition.split()[-1])

            if ">" in alert.condition:
                send_alert = (value > compare_value)
            elif alert["condition"] == "<":
                send_alert = (value < compare_value)
            elif alert["condition"] == "=":
                send_alert = (value == compare_value)

            if send_alert:
                message = angle_brackets_replace_specific()
                a['message'] = (angle_brackets_replace_specific(
                    a["message"], "alias", room
                                    + "(" + get_psid_from_alias(
                                        room,
                                        alert["building"],
                                        alert["type"]) + ")"))
                
                event_id = assign_event_id(new_events, alert,
                                           data[id_column][i])
                self.anomalies.append(Anomaly(alert.type,)) # TODO
        return None


    def check_temp(self, alert, building):
        """Check relative temperature values."""
        selection_command = (f"SELECT * FROM "
                             f"CEVAC_{building}_TEMP_"
                             f"{alert.aggregation}")
        data = pd.read_sql_query(selection_command, self.conn)

        # Combine set points and rooms
        temps = {}
        for i in range(len(data)):
            alias = data["Alias"][i]
            value = data["ActualValue"][i]
            room = alias.split()[1]
            if room in temps:
                if "Cooling SP" in alias:
                    temps[room]["Cooling SP"] = value
                elif "Heating SP" in alias:
                    temps[room]["Heating SP"] = value
                else:
                    temps[room]["Room"] = alias
                    temps[room][alias] = value
            else:
                if "Cooling SP" in alias:
                    temps[room] = {"Cooling SP": value}
                elif "Heating SP" in alias:
                    temps[room] = {"Heating SP": value}
                else:
                    temps[room] = {"Room": alias}
                    temps[room][alias] = value
                        
        for room in temps:
            for val in ["Room"]:
                if val not in temps[room]:
                    continue

            # Modify value
            room_vals = temps[room]
            val = float(room_vals.split()[-1])
            try:
                if "+" in alert.condition:
                    room_vals["Cooling SP"] += val
                    room_vals["Heating SP"] += val
                elif "-" in alert.condition.split():
                    room_vals["Cooling SP"] -= val
                    room_vals["Heating SP"] -= val

            # Check value
            send_alert = False

            if ">" in alert.condition:
                if "@CoolingSP" in alert.condition:
                    if "Cooling SP" in room_vals:
                        send_alert = (
                            room_vals["Cooling SP"] <
                            room_vals[room_vals["Room"]])
                if "@HeatingSP" in alert.condition:
                    if "Heating SP" in room_vals:
                        send_alert = (
                            room_vals["Heating SP"] <
                            room_vals[room_vals["Room"]])
            elif "<" in alert.condition:
                if "@CoolingSP" in alert.condition:
                    if "Cooling SP" in room_vals:
                        send_alert = (
                            room_vals["Cooling SP"] >
                            room_vals[room_vals["Room"]])
                if "@HeatingSP" in alert.condition:
                    if "Heating SP" in room_vals:
                        send_alert = (
                            room_vals["Heating SP"] >
                            room_vals[room_vals["Room"]])

            if send_alert:
                message = angle_brackets_replace_specific()
                            
                event_id = assign_event_id(new_events, alert,
                                           data[id_column][i])
                self.anomalies.append(Anomaly(alert.type,)) # TODO
        return None

    def check_time(self, alert, building):
        """Check time off since last report."""
        selection_command = ("Select Alias, ActualValue FROM "
                             f"CEVAC_{building}_{alert.metric}_"
                             f"{Aggregation}_BROKEN_CACHE")
        data = pd.read_sql_query(data, self.conn)

        for i in range(len(data)):
            alias = data["Alias"][i]
            days_since = data["ActualValue"][i]

            assign_event_id()  # TODO
            self.anomalies.append(Anomaly())  # TODO

        return None

    def table_exists(self, metric, bldg_s_name, aggregation):
        """True if table exists.
        
        TODO: Debug this.
        """
        if aggregation is not "":
            aggregation = f"_{aggregation}"
        comm = ("SELECT COUNT(*) FROM "
                "information_schema.tables WHERE"
                "TABLE_NAME = "
                f"'CEVAC_{metric}_{bldg_s_name}{aggregation}'")
        x = pd.read_sql_query(comm, self.conn)
        if x[0] == 1:
            return True
        return False

    def building_s_list(self):
        """Return list of buildings (s names)."""
        comm = "SELECT BuildingSName FROM CEVAC_BUILDING_INFO"
        data = pd.read_sql_query(comm, self.conn)
        return data['BuildingSName']

    def skip_building(self, building, alert):
        occupied = self.occ.building_is_occupied(bulding)
        if alert.occupancy.lower() == "true" and not occupied:
            return True
        elif alert.occupancy.lower() == "false" and occupied:
            return True
        else:
            return False

    def safe_log(self, message, condition):
        if self.LOG:
            if "error" in condition.lower():
                self.logging.error(message)
            else:
                self.logging.info(message)

    def __del__(self):
        """Deconstructor."""
        self.conn.close()


class Anomaly:
    """All issues become anomalie objects."""
    def __init__(self, alert_type, alert_message, metric, bldg_d_name, datetime, message_id, alias, event_id, bldg_s_name):
        self.alert_type = ""  # time, abs, tempsp...
        self.alert_message = alert_message
        self.metric = metric
        self.UTCDateTime = datetime
        self.message_id = message_id
        self.alias = alias
        self.event_id = event_id
        self.bldg_d_name = bldg_d_name
        self.bldg_s_name = bldg_s_name

    def insert(self, cursor):
        cursor.execute("insert into CEVAC_ALL_ALERTS_HIST_RAW (AlertType, "
                       "AlertMessage, Metric, BuildingDName, UTCDateTime, "
                       "MessageID, Alias, EventID, BuildingSName), "
                       "(?,?,?,?,?,?,?,?,?)",
                       [()])


class Occupancy:
    """Simple singleton to maintain occupancy data.
    
    Note: this is complete.
    """

    def __init__(self, conn):
        """Initialize building_occupied map."""
        data = pd.read_sql_query("SELECT * FROM CEVAC_OCCUPANCY", conn)
        self.building_occupied = {"*": False}
        for i in range(len(data)):
            crontab = (f"{data['Minutes'][i]} {data['Hour'][i]} "
                       f"{data['Day_month'][i]} "
                       f"{data['Month'][i]} {data['Day_week'][i]}")
            if data['Cron_Occupancy'][i]:
                if not self.cron_is_now(crontab):
                    continue
                if "*" in data["BuildingSName"][i]:
                    for item in self.building_occupied:
                        self.building_occupied[item] = data['Occupied'][i]
                    self.building_occupied["*"] = data['Occupied'][i]
                else:
                    self.building_occupied[
                        data["BuildingSName"][i]] = data['Occupied'][i]

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
        data = pd.read_sql_query("SELECT * FROM CEVAC_ALERT_PARAMETERS", conn)
        self.alert_parameters = []
        for i, in range(len(data)):
            self.alert_parameters.append({
                "metric": data['Metric'][i].strip(),
                "condition": data['Condition'][i].strip(),
                "message": data['Message'][i].strip(),
                "importance": data['Importance'][i].strip(),
                "occupancy": data['Occupancy'][i].strip(),
                "alis-psid": data['alias-psid'][i].strip(),
            })



class Known_Issues:
    """Represents known issues to ignore."""
    
    def __init__(self, conn):
        """Initialize known issues."""
        data = pd.read_sql_query("SELECT * FROM CEVAC_KNOWN_ISSUES", conn)
        self.alias_psid = {}
        for i in range(len(data)):
            if 'decomissioned' in data['Code'][i].lower():
                self.alias_psid[data['Alias-PSID']] = None

    def check_aliaspsid(self, aliaspsid):
        return (aliaspsid in self.alias_psid)
        


def rebuild_broken_cache(table):
    """Rebuild a broken cache."""
    if "LATEST" not in table:
        print("LATEST NOT IN TABLE NAME")
        return None
    broken = "_BROKEN"
    command = f"EXEC CEVAC_CACHE_INIT @tables = '{table+broken}'"
    print(command)
    os.system("/cevac/scripts/exec_sql.sh \"" + command +
              "\" temp_csv.csv")
    return None


def verbose_print(verbose, message):
    """Print message if verbose is True.
    
    Returns whether or not the message printed.
    """
    if verbose:
        print(message)
        return True
    return False


# For debugging
if __name__ == "__main__":
    print("DEBUG ALERT SYSTEM")
    all_alerts = Alerts(None, verbose=True)
    all_alerts.alert_system()
    
    print(all_alerts.occ.building_occupied)
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
