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


class Alert:
    def __init__(self, verbose=False):
        self.message = ""
        self.verbose = verbose


class Alerts:
    def __init__(self, verbose=False):
        conn = None  # TODO
        self.occ = Occupancy(conn)
        self.par = Parameters(conn)
        self.known_issues = Known_Issues(conn)
        self.verbose = verbose
        self.all_alerts = []
        self.anomalies = []

    def alert_system(self):
        """Find and catalog all anomalies."""
        print("Will run alert system.")


class Anomalie:
    def __init__(self, actual_value, alert, psid):
        self.psid = psid
        self.alert = alert
        self.actual_value = actual_value


class Occupancy:
    def __init__(self, conn):
        pass


class Parameters:
    def __init__(self, conn):
        pass


class Known_Issues:
    def __init__(self, conn):
        pass


def angle_brackets_replace_specific(regex_string, key, replacement):
    """Return string with angle brackets at key replaced with replacement."""
    try:
        regex_list = regex_string.split(f"<{key}>")
        for i, regex in enumerate(regex_list):
            if i < len(regex_list) - 1:
                regex_list[i] += str(replacement)
        return "".join(regex_list)
    except Exception:
        return regex_string


def skip_alias(known_issues, bldg, alias, metric):
    """Check known issues for decomissioned alias."""
    psid = get_psid_from_alias(alias, bldg, metric)
    if bldg not in known_issues:
        return False
    for message in known_issues[bldg]:
        if f"({psid})" in message:
            return True
    return False


def cron_is_now(cron, offset=5):
    """Return True if cron is within 5 minutes of now."""
    now = datetime.datetime.utcnow()
    c = croniter(cron)
    td = (now - c.get_next(datetime.datetime))
    td_min = abs(td.total_seconds()/60)
    if td_min < offset:
        return True
    return False


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


def parse_json(*filenames):
    """Parse json(s) for cron use."""
    max_id = 0
    new_json = {}
    for filename in filenames:
        try:
            f = open(filename, "r")
            line = f.readlines()[0]
            new_json.update(json.loads(line))
            next_id = new_json["next_id"]
            max_id = max(max_id, next_id)
            f.close()
        except Exception:
            continue
    return (max_id, new_json)


def write_json_generic(new_events, next_id):
    """Write json independent of time."""
    new_events["next_id"] = next_id
    if is_occupied():
        f = open(json_oc, "w")
    else:
        f = open(json_unoc, "w")
    f.write(json.dumps(new_events))
    f.close()
    return None


def assign_event_id(next_id, old_json, new_json, alert, alias):
    """Assign event id."""
    key = alias+alert["message_id"]
    event_id = next_id
    if key in old_json:
        event_id = old_json[key]
        new_json[key] = event_id
    else:
        next_id += 1
        new_json[key] = event_id
    return event_id, next_id, new_json


def get_alias_or_psid(table_name):
    """Return whether a table uses alias or point slice id."""
    request_str = f"EXEC CEVAC_ALIAS_OR_PSID @table = '{table_name}'"
    r_dict = json.loads(command_to_json_string(request_str).replace("'", '"'))
    for key in r_dict:
        return r_dict[key]


def is_occupied():
    """Return True if in occupied time."""
    now = datetime.datetime.now()
    day = now.isoweekday()
    hour = now.hour
    correct_day = (day >= 1 and day <= 5)
    correct_hour = (hour >= 8 and hour < 17)
    if (correct_day and correct_hour):
        return True
    return False


def get_psid_from_alias(alias, bldgsname, metric):
    """Return the (most recent) pointsliceid from an alias."""
    print(f"get psid from alias: {alias} {bldgsname} {metric}")
    try:
        command = (f"EXEC CEVAC_XREF_LOOKUP @BuildingSName = '{bldgsname}', "
                   f"@Metric = '{metric}', @Alias = '{alias}'")
        os.system("/cevac/scripts/exec_sql.sh \"" + command +
                  "\" temp_psid_csv.csv")
        f = open("/cevac/cache/temp_psid_csv.csv", "r")
        lines = f.readlines()
        try:
            psids = [int(psid.replace("\n", "")) for i,
                     psid in enumerate(lines) if i > 0]
            os.remove("/cevac/cache/temp_psid_csv.csv")
            return str(max(psids))
        except Exception:
            os.remove("/cevac/cache/temp_psid_csv.csv")
            return str(int(lines[-1].replace("\n", "")))
    except Exception:
        print("could not get psid from alias")
        os.remove("/cevac/cache/temp_psid_csv.csv")
        return ""


def building_is_occupied(occupancy_dict, building):
    """Return True if in occupied time."""
    if occupancy_dict is None:
        now = datetime.datetime.now()
        day = now.isoweekday()
        hour = now.hour
        correct_day = (day >= 1 and day <= 5)
        correct_hour = (hour >= 8 and hour < 17)
        if (correct_day and correct_hour):
            return True
        return False
    elif building not in occupancy_dict:
        return occupancy_dict["*"]
    else:
        return occupancy_dict[building]
    return False


def check_numerical_alias(alias, alert, next_id, last_events, new_events,
                          get_psid):
    """Check numerical alias alert."""
    selection_command = (f"SELECT TOP {str(alert['num_entries'])} "
                         f"{alert['column']} FROM "
                         f"{str(alert['database'])}")
    if alert["aliases"] == ["*"]:
        selection_command += f" WHERE {a_or_psid} = '{alias}'"
        selection_command += f" ORDER BY {alert['sort_column']} DESC"
    else:
        rem_a = str(alert['aliases']).replace('[', '').replace(']', '')
        selection_command += (f" WHERE ALIAS IN "
                              f"({rem_a}) AND Alias = '{alias}'"
                              f" ORDER BY {alert['sort_column']} DESC")

    print(selection_command)
    if not CHECK_ALERTS:
        return (next_id, new_events, "")

    data_list = command_to_list_single(selection_command)
    data_list = [float(d) for d in data_list]
    avg_data = sum(data_list) / len(data_list)

    send_alert = False
    if alert["condition"] == ">":
        send_alert = (avg_data > alert["value"])
    elif alert["condition"] == "<":
        send_alert = (avg_data < alert["value"])
    elif alert["condition"] == "=":
        send_alert = (avg_data == alert["value"])

    alias = "Alias"
    if send_alert:
        a = deepcopy(alert)
        if get_psid:
            a['message'] = (angle_brackets_replace_specific(
                            a["message"], "alias", room
                            + "(" + get_psid_from_alias(
                                    room,
                                    alert["building"],
                                    alert["type"]) + ")"))
        else:
            a['message'] = (angle_brackets_replace_specific(
                            a["message"], "alias", room))
        event_id, next_id, new_events = assign_event_id(next_id,
                                                        last_events,
                                                        new_events,
                                                        alert,
                                                        alias)
        safe_log("An alert was sent for " + str(alert), "info")
        com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
               f"AlertMessage, Metric, BuildingDName, UTCDateTime, "
               "MessageID, "
               "Alias, EventID, BuildingSName) "
               f"VALUES('{alert['operation']}',"
               f"'{a['message']}',"
               f"'{alert['type']}',"
               f"'{alert['bldg_disp']}','{utcdatetimenow_str}',"
               f"'{alert['message_id']}', {alias}, '{event_id}',"
               f"'{alert['building']}')")
    return (next_id, new_events, com + ";")


def check_temp(room, alert, temps, known_issues, next_id, last_events,
               new_events, get_psid):
    """Check relative temperature values."""
    if skip_alias(known_issues, alert["building"], room, "TEMP"):
        print(room, " is decomissioned")
        return (next_id, new_events, "")
    else:
        pass

    try:
        Alias_Temp = "Temp"
        for key in temps[room].keys():
            if (key != "Cooling SP" and key != "Heating SP"
                    and "TEMP" in key):
                Alias_Temp = key
            elif ("AHU" in key):
                continue
            else:
                continue

        # Modify value
        room_vals = temps[room]
        val = 0
        try:
            if "+" in alert["value"]:
                val_str = alert["value"].split()[-1]
                val = float(val_str[val_str.find("+") + 1:])
                room_vals["Cooling SP"] += val
                room_vals["Heating SP"] += val
            elif "-" in alert["value"].split():
                val_str = alert["value"].split()[-1]
                val = float(val_str[val_str.find("-") + 1:])
                room_vals["Cooling SP"] -= val
                room_vals["Heating SP"] -= val
        except Exception:
            return (next_id, new_events, "")

        # Check value
        send_alert = False

        if ">" in alert["condition"]:
            if "Cooling SP" in alert["value"]:
                if "Cooling SP" in room_vals:
                    send_alert = (
                        room_vals["Cooling SP"] <
                        room_vals[Alias_Temp])
            if "Heating SP" in alert["value"]:
                if "Heating SP" in room_vals:
                    send_alert = (
                        room_vals["Heating SP"] <
                        room_vals[Alias_Temp])
        elif "<" in alert["condition"]:
            if "Cooling SP" in alert["value"]:
                if "Cooling SP" in room_vals:
                    send_alert = (
                        room_vals["Cooling SP"] >
                        room_vals[Alias_Temp])
            if "Heating SP" in alert["value"]:
                if "Heating SP" in room_vals:
                    send_alert = (
                        room_vals["Heating SP"] >
                        room_vals[Alias_Temp])

        if send_alert:
            a = deepcopy(alert)
            add = get_psid_from_alias(room + " Temp", alert["building"],
                                      alert["type"]) if get_psid else ""
            a["message"] = angle_brackets_replace_specific(
                            a["message"], "alias",
                            room + " Temp (" + add + ")")
            a["message"] = angle_brackets_replace_specific(
                            a["message"], "Cooling SP",
                            f"{(room_vals['Cooling SP']-val):.1f}")
            a["message"] = angle_brackets_replace_specific(
                            a["message"], "Heating SP",
                            f"{(room_vals['Heating SP']+val):.1f}")
            a["message"] = angle_brackets_replace_specific(
                            a["message"], "ActualValue",
                            f"{room_vals[Alias_Temp]:.1f}")

            event_id, next_id, new_events = assign_event_id(
                                                next_id,
                                                last_events,
                                                new_events,
                                                alert, room)

            com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW("
                   f"AlertType,"
                   f" AlertMessage, Metric,BuildingDName,"
                   "UTCDateTime,"
                   f"MessageID, Alias, EventID, BuildingSName)"
                   f" VALUES('{a['operation']}','{a['message']}',"
                   f"'{a['type']}','{a['bldg_disp']}',"
                   f"'{utcdatetimenow_str}',"
                   f"'{alert['message_id']}', '{room}', "
                   f"'{event_id}', '{alert['building']}')")
            safe_log("An alert was sent for " + str(a), "info")
            return (next_id, new_events, com + ";")
    except Exception:
        pass

    return (next_id, new_events, "")


def check_time(data, alert, next_id, last_events, new_events, get_psid):
    """Check time off since last report."""
    alias = data
    if skip_alias(known_issues, alert["building"], alias, alert["type"]):
        print(alias, " is decomissioned")
        return (next_id, new_events, "")
    else:
        pass
    t = aliases[alias]

    datetime_object = datetime.datetime.strptime(
        t, '%Y-%m-%d %H:%M:%S.%f')
    now_aware = pytz.utc.localize(datetime_object)
    today = datetime.datetime.now()
    today = pytz.utc.localize(today)
    time_diff = (today - now_aware)
    days_since = time_diff.days + 1  # ceil

    # Add to alerts to send
    safe_log("An alert was sent for " + str(alert), "info")
    a = deepcopy(alert)
    add = (" (" + get_psid_from_alias(alias, alert["building"], alert["type"])
           + ")" if get_psid else "")
    a["message"] = angle_brackets_replace_specific(
                        a["message"], "alias", alias + add)
    a["message"] = angle_brackets_replace_specific(
                        a["message"], "days", days_since)
    event_id, next_id, new_events = assign_event_id(
                                        next_id,
                                        last_events,
                                        new_events,
                                        alert,
                                        alias)
    print(a["message"])

    com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
           f"AlertMessage, Metric,BuildingDName,UTCDateTime, "
           f"MessageID, Alias, EventID, BuildingSName)"
           f" VALUES('{a['operation']}','{a['message']}',"
           f"'{a['type']}','{a['bldg_disp']}',"
           f"'{utcdatetimenow_str}',"
           f"'{alert['message_id']}', '{alias}',"
           f" '{event_id}', '{alert['building']}')")
    return (next_id, new_events, com + "; ")


if __name__ == "__main__":
    # Initialize logging
    if LOG:
        FORMAT = '%(asctime)s %(levelname)s:%(message)s'
        datestring = str(datetime.datetime.now().date())
        log_file = os.path.join(LOGGING_PATH, datestring + '.log')
        logging.basicConfig(filename=log_file, format=FORMAT,
                            level=logging.INFO)
        logging.info("NEW JOB\n---")

    # Get alert conditions
    alerts, unique_databases = import_conditions(alert_fname, logging)
    known_issues = import_known_issues(KNOWN_ISSUES_FPATH)
    occupancy = import_occupancy()

    # Parse json files for event IDs
    next_id, last_events = parse_json(json_oc, json_unoc)
    new_events = {}  # id: { "hash" : event_id }

    # Check alerts for conditions
    insert_sql_total = ""  # SQL to be inserted
    utcdatetimenow = datetime.datetime.utcnow()
    utcdatetimenow_str = sql_time_str(utcdatetimenow)
    for i, a in enumerate(alerts):
        alert = alerts[a]
        a_or_psid = get_alias_or_psid(alert["database"])
        get_psid = (a_or_psid == "Alias")
        try:
            # Check time conditional to make sure it is the correct time for
            # the alert
            now = datetime.datetime.now()
            day = now.isoweekday()
            hour = now.hour
            occupied = building_is_occupied(occupancy, alert["building"])
            if (alert["time_dependent"]):
                if ((alert["occupancy_status"] and (not occupied))
                        or (not alert["occupancy_status"] and (occupied))):
                    safe_log("Not time for alert #" + str(i + 1), "info")
                    continue

            # Check basic value for basic alert
            if str.isdigit(alert["value"]):
                alert["value"] = float(alert["value"])
                z = (f"SELECT DISTINCT "
                     f"{a_or_psid} "
                     f"FROM {alert['database']}")
                z = command_to_list_multiple(z, 2)
                all_aliases = [b[0] for b in z]

                for alias in all_aliases:
                    try:
                        obj = check_numerical_alias(alias, alert,
                                                    next_id,
                                                    last_events,
                                                    new_events, get_psid)
                        next_id = obj[0]
                        new_events = obj[1]
                        insert_sql_total += obj[2]
                    except Exception:
                        pass

            # Check each alias for relative temperature exceptions
            elif ("SP" in alert["value"]):
                selection_command = (f"SELECT {a_or_psid}, {alert['column']} "
                                     f"FROM "
                                     f"{alert['database']} ORDER BY "
                                     f"{alert['sort_column']}")
                print(selection_command)

                if not CHECK_ALERTS:
                    continue

                data_list = command_to_list_multiple(selection_command, 2)

                temps = {}
                ec = 0
                for row in data_list:
                    try:
                        room = row[0].split()[0]
                        if room in temps:
                            temps[room][row[0][row[0].find(
                                " ") + 1:]] = float(row[1])
                        else:
                            temps[room] = {
                                row[0][row[0].find(" ") + 1:]: float(row[1])
                            }
                    except Exception:
                        ec += 1

                for room in temps:
                    obj = check_temp(room, alert, temps,
                                     known_issues,
                                     next_id, last_events,
                                     new_events, get_psid)
                    next_id = obj[0]
                    new_events = obj[1]
                    insert_sql_total += obj[2]

            # Check if aliases have reported within a given time
            elif ("<now>" in alert["value"]):
                # Find all aliases
                selection_command = (f"SELECT {a_or_psid}, UTCDateTime FROM "
                                     f"{alert['database']+'_BROKEN_CACHE'}")
                print(selection_command)
                if not CHECK_ALERTS:
                    continue

                if UPDATE_CACHE:
                    rebuild_broken_cache(alert["database"])

                try:
                    data_list = command_to_list_multiple(selection_command, 2)
                except Exception:
                    continue

                aliases = {}
                for data in data_list:
                    aliases[data[0]] = data[1]

                # alert["value"] in format "<now> - # day/hr/min"
                dst = False
                local = pytz.timezone("America/New_York")
                naive = datetime.datetime.now()
                local_dt = local.localize(naive, is_dst=dst)
                utc_dt = local_dt.astimezone(pytz.utc)
                try:
                    amount = int(alert["value"].split()[2])
                    unit_str = alert["value"].split()[3]
                    unit = TIME[unit_str]
                except Exception:
                    amount = 1
                    unit = TIME["hour"]
                minutes = amount * 24 * 60 / unit

                for data in aliases:
                    obj = check_time(data, alert, next_id, last_events,
                                     new_events, get_psid)
                    next_id = obj[0]
                    new_events = obj[1]
                    insert_sql_total += obj[2]
            else:
                safe_log("Could not find valid condition/value for " +
                         str(alert), "info")
                print("invalid condition")

        except Exception:
            safe_log("Issue on alert " + str(i + 2) + " " + str(alert),
                     "error")
            print("issue on alert", str(i + 2))

    if insert_sql_total == "":
        insert_sql_total = ("INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType,"
                            "AlertMessage,Metric,UTCDateTime,MessageID) "
                            f"VALUES('All Clear','All Clear','N/A',"
                            f"GETUTCDATE(),'0')")

    # Insert into CEVAC_ALL_ALERTS_HIST
    if LOG:
        write_json_generic(new_events, next_id)
    if SEND:
        f = open("/cevac/cache/insert_alert_system.sql", "w")
        f.write(insert_sql_total.replace(';', '\nGO\n'))
        f.close()
        os.system("/cevac/scripts/exec_sql_script.sh "
                  "/cevac/cache/insert_alert_system.sql")
    else:
        print(insert_sql_total.replace(';', '\nGO\n'))

    if LOG:
        logging.info(str(datetime.datetime.now()))
        logging.shutdown()

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
