"""CEVAC Alert System alert_system.py.

This CEVAC alert system script reads from alert_system.csv to populate the
table `CEVAC_ALL_ALERTS_HIST`.
"""

import os
import csv
import json
import datetime
import pytz
import logging
from copy import deepcopy
from croniter import croniter


CONDITIONS_FPATH = "/cevac/cron/alerts/"
KNOWN_ISSUES_FPATH = "/cevac/DEV/known issues/Known Data Issues.csv"
OCCUPANCY_FPATH = "/cevac/CEVAC/scripts/harrison/alerts/occupancy.csv"
LOGGING_PATH = "/cevac/cron/alerts/"
PHONE_PATH = "/cevac/cron/alerts/"
alert_fname = "/cevac/DEV/alerts/alert_parameters.csv"
json_oc = "/cevac/cron/alert_log_oc.json"
json_unoc = "/cevac/cron/alert_log_unoc.json"

# Determines whether or not to write a log and keep track of event id's
LOG = True

# Determines whether or not to check the alerts against the respectful
# databases
CHECK_ALERTS = True

# Determines whether or not to insert the found alerts into the alert databse
SEND = True

# Determines whether or not to update the cache alerts are checked against
UPDATE_CACHE = True

# The positions for columns in the csv
COLUMNS = {
    "alert_name": 0,
    "type": 1,
    "aliases": 2,
    "unit": 3,
    "message": 4,
    "building": 5,
    "bldg_disp": 6,
    "database": 7,
    "column": 8,
    "sort_column": 9,
    "num_entries": 10,
    "time_dependent": 11,
    "occupancy_status": 12,
    "condition": 13,
    "value": 14,
    "operation": 15,
    "message_id": 16,
}

# Time constants
TIME = {
    "day": 1,
    "hr": 24,
    "hour": 24,
    "min": 24 * 60,
    "minute": 24 * 60,
    "minutes": 24 * 60,
}


def sql_time_str(t):
    """Return time in sql format."""
    return t.strftime('%Y-%m-%d %H:%M:%S')


def debug_print(message):
    """Print message if in debug mode."""
    if not CHECK_ALERTS or not SEND:
        print(message)
    return None


def alias_to_list(regex_string):
    """Return a list of strings that were originally seperated by hyphens."""
    if regex_string == "*":
        return ["*"]
    return regex_string.split("-")


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


def import_conditions(fname, logger):
    """Move a CSV file to dict of alert condtions."""
    alerts = {}
    unique_databases = {}
    with open(fname) as csvfile:
        csvfile = csv.reader(csvfile)
        next(csvfile)
        for i, row in enumerate(csvfile):
            try:
                if (i >= 0):
                    alerts[row[COLUMNS["alert_name"]]] = {
                        "type": row[COLUMNS["type"]],
                        "message": row[COLUMNS["message"]],
                        "database": row[COLUMNS["database"]],
                        "column": row[COLUMNS["column"]],
                        "num_entries": int(row[COLUMNS["num_entries"]]),
                        "time_dependent": int(row[COLUMNS["time_dependent"]]),
                        "occupancy_status": (int(
                                            row[COLUMNS["occupancy_status"]])
                                             if row[COLUMNS["occupancy_status"]
                                                    ] != "*" else 0),
                        "condition": row[COLUMNS["condition"]],
                        "value": row[COLUMNS["value"]],
                        "operation": row[COLUMNS["operation"]],
                        "aliases": alias_to_list(row[COLUMNS["aliases"]]),
                        "sort_column": row[COLUMNS["sort_column"]],
                        "building": row[COLUMNS["building"]],
                        "bldg_disp": row[COLUMNS["bldg_disp"]],
                        "message_id": row[COLUMNS["message_id"]]
                    }
                    unique_databases[row[COLUMNS["database"]]] = None
            except Exception:
                safe_log("Issue importing conditions " + str(i), "error")
    return (alerts, unique_databases)


def import_known_issues(fname):
    """Return dict of buildingsname to list of blacklist messages."""
    d = {}
    with open(fname, "r") as csvfile:
        csvfile = csv.reader(csvfile)
        next(csvfile)  # header
        for row in csvfile:
            try:
                bldg = row[1]
                message = row[0]
                if "decommissioned" in message:
                    # psid = bldg.replace(")", "(").split("(")[1]
                    # debug_print("Found PSID as", psid)
                    if bldg in d:
                        d[bldg].append(message)
                    else:
                        d[bldg] = [message]
            except Exception:
                continue
    return d


def skip_alias(known_issues, bldg, alias):
    """Check known issues for decomissioned alias."""
    if bldg not in known_issues:
        return False
    for message in known_issues[bldg]:
        if f"{alias}" in message:
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


def str_to_bool(some_str):
    """Return True/False for 'true/false'."""
    if "true" in some_str.lower():
        return True
    return False


def import_occupancy():
    """Import occupancy for each building."""
    d = {"*": False}
    past_header = False
    with open(OCCUPANCY_FPATH, "r") as csvfile:
        csvfile = csv.reader(csvfile)
        for row in csvfile:
            if ("BuildingSName" in row[0]):
                past_header = True
                continue
            if not past_header:
                continue
            try:
                bldgsname = row[0]
                cron_occupancy = str_to_bool(row[2])
                is_occupied = str_to_bool(row[3])
                crontab = f"{row[4]} {row[5]} {row[6]} {row[7]} {row[8]}"
                if cron_is_now(crontab) and cron_occupancy:
                    if "*" in bldgsname:
                        for item in d:
                            d[item] = is_occupied
                        d["*"] = is_occupied
                    else:
                        d[bldgsname] = is_occupied
            except Exception:
                continue

    return d


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


def command_to_json_string(command):
    """Return a string of json from a sql command."""
    os.system("/cevac/scripts/exec_sql.sh \"" + command +
              "\" temp_csv.csv")

    json_string = ""
    headers = {}
    with open("/cevac/cache/temp_csv.csv", "r") as temp_csv:
        csvfile = csv.reader(temp_csv)
        for i, row in enumerate(csvfile):
            if i == 0:
                for j, item in enumerate(row):
                    headers[j] = item
            else:
                temp_dict = {}
                try:
                    for j, item in enumerate(row):
                        temp_dict[headers[j]] = item
                    json_string += str(temp_dict)
                except Exception:
                    continue

    return json_string


def command_to_list_single(command):
    """Return a list of data from a query."""
    data = command_to_json_string(command)
    data_readable = data.replace("}{", "} {").replace("\'", "\"")
    data_list = data_readable.split("} {")
    dict_list = [json.loads(d) for d in data_list]
    data_list = [sd[list(sd.keys())[0]] for sd in dict_list]
    return data_list


def command_to_list_multiple(command, num_args):
    """Return a list of lists.

    list of lists (with length up to num_args) of data from a query.
    This can break if the SQL server is manipulating the data currently.
    """
    data = command_to_json_string(command)
    data_readable = data.replace("}{", "} {").replace("\'", "\"")
    data_list = data_readable.split("} {")
    dict_list = []
    try:
        for i, d in enumerate(data_list):
            d = d if d[0] == "{" else "{" + d
            d = d if d[-1] == "}" else d + "}"
            dict_list.append(json.loads(d))
    except Exception:
        print("issue, data:")
        print(data_list)
    data_list = []
    for sd in dict_list:
        try:
            dl = []
            for k in sd:
                dl.append(sd[k])
            data_list.append(dl)
        except Exception:
            print(Exception, data_list)
    return data_list


def safe_log(message, type):
    """Log a message safely."""
    if LOG:
        if type.lower() == "error":
            logging.error(message)
        else:
            logging.info(message)


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
    if is_occupied():
        write_json(json_oc, new_events, next_id)
    else:
        write_json(json_unoc, new_events, next_id)
    return None


def write_json(filename, new_events, next_id):
    """Write json to file."""
    new_events["next_id"] = next_id
    f = open(filename, "w")
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


def check_numerical_alias(alias, alert, next_id, last_events, new_events, get_psid):
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
            a['message'] = angle_brackets_replace_specific(a["message"], "alias",
                                        room
                                        + "(" + get_psid_from_alias(room,
                                                              alert["building"],
                                                              alert["type"]) + ")")
        else:
            a['message'] = angle_brackets_replace_specific(a["message"], "alias",
                                        room)
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


def check_temp(room, alert, temps, known_issues, next_id, last_events, new_events, get_psid):
    """Check relative temperature values."""
    if skip_alias(known_issues, alert["building"], room):
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
            add = get_psid_from_alias(room + " Temp", alert["building"], alert["type"]) if get_psid else ""
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
    if skip_alias(known_issues, alert["building"], alias):
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
    add = " (" +get_psid_from_alias(alias, alert["building"],alert["type"]) + ")" if get_psid else ""
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
