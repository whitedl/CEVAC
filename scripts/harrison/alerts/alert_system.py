"""CEVAC Alert System alert_system.py.

This CEVAC alert system script reads from alert_system.csv to populate the
table `CEVAC_ALL_ALERTS_HIST`.
"""

import os
import sys
import csv
import json
import datetime
import pytz
import logging
from copy import deepcopy
from croniter import croniter

CONDITIONS_FPATH = "/home/bmeares/cron/alerts/"
KNOWN_ISSUES_FPATH = "/cevac/DEV/known issues/Known Data Issues.csv"
OCCUPANCY_FPATH = "/cevac/CEVAC/scripts/harrison/alerts/occupancy.csv"
LOGGING_PATH = "/home/bmeares/cron/alerts/"
PHONE_PATH = "/home/bmeares/cron/alerts/"
alert_fname = "/cevac/CEVAC/alerts/alert_parameters.csv"
json_fname = "/cevac/cron/alert_log.json"
json_oc = "/cevac/cron/alert_log_oc.json"
json_unoc = "/cevac/cron/alert_log_unoc.json"


LOG = False
CHECK_ALERTS = True
SEND = False
UPDATE_CACHE = False

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


def regex_to_numlist(regex_string):
    """Return a num_list.

    A list of numbers following expressions similar to "1-5 & 9-10" to
    [1,2,3,4,5,9,10].
    """
    if regex_string == "*":
        return [regex_string]
    else:
        rs = regex_string.replace(" ", "").split("&")
        regex_list = [([int(y)] if len(
                                y.split("-")) == 1 else list(range(
                                    int(y.split("-")[0]),
                                    int(y.split("-")[1]) + 1))) for y in rs]
        return_list = []
        for num_list in regex_list:
            for num in num_list:
                return_list.append(str(num))
        return return_list


def alias_to_list(regex_string):
    """Return a list of strings that were originally seperated by hyphens."""
    if regex_string == "*":
        return ["*"]
    return regex_string.split("-")


def angle_brackets_replace(regex_string, alert):
    """Return string with angle brackets replaced."""
    lc_alert = {}
    for key in alert:
        lc_alert[key.lower()] = alert[key]
    try:
        regex_list = regex_string.replace(">", "<").split("<")
        for i, regex in enumerate(regex_list):
            if regex.lower() in lc_alert:
                regex_list[i] = lc_alert[regex]
        return "".join(regex_list)
    except Exception:
        return regex_string


def angle_brackets_replace_single(regex_string, replacement):
    """Return string with angle brackets replaced with replacement."""
    try:
        regex_list = regex_string.replace(
            "<", "<&%").replace(">", "<").split("<")
        for i, regex in enumerate(regex_list):
            if "&%" in regex:
                regex_list[i] = replacement
        return "".join(regex_list)
    except Exception:
        return regex_string


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
    """Return dict of buildingsname to list of blacklists."""
    d = {}
    with open(fname, "r") as csvfile:
        csvfile = csv.reader(csvfile)
        next(csvfile)  # header
        for row in csvfile:
            bldg = row[1]
            message = row[0]
            if "decomissioned" in message:
                if bldg in d:
                    d[bldg].append(message)
                else:
                    d[bldg] = [message]
    return d


def skip_alias(known_issues, bldg, alias):
    """Check known issues for decomissioned alias."""
    if bldg not in known_issues:
        return False
    for message in known_issues[bldg]:
        if alias in message:
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
    os.system("/home/bmeares/scripts/exec_sql.sh \"" + command +
              "\" temp_csv.csv")
    return None


def command_to_json_string(command):
    """Return a string of json from a sql command."""
    os.system("/home/bmeares/scripts/exec_sql.sh \"" + command +
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
    """
    data = command_to_json_string(command)

    data_readable = data.replace("}{", "} {").replace("\'", "\"")
    data_list = data_readable.split("} {")
    dict_list = []
    for i, d in enumerate(data_list):
        d = d if d[0] == "{" else "{" + d
        d = d if d[-1] == "}" else d + "}"
        dict_list.append(json.loads(d))

    data_list = []
    for sd in dict_list:
        try:
            dl = []
            for k in sd:
                dl.append(sd[k])
            data_list.append(dl)
        except Exception:
            pass
    return data_list


def safe_log(message, type):
    """Log a message safely."""
    if LOG:
        if type == "error":
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


def check_numerical_alias(alias, alert, next_id, last_events, new_events):
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
        return ""

    data_list = command_to_list_single(selection_command)
    data_list = [float(d) for d in data_list]
    avg_data = sum(data_list) / len(data_list)

    send_alert = False
    if alert["condition"] == ">":
        send_alert = (avg_data > alert["value"])
    elif alert["condition"] == "<":
        send_alert = (avg_data < alert["value"])

    alias = "Alias"
    if send_alert:
        event_id, next_id, new_events = assign_event_id(next_id,
                                                        last_events,
                                                        new_events,
                                                        alert,
                                                        alias)
        safe_log("An alert was sent for " + str(alert), "info")
        com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
               f"AlertMessage, Metric, BuildingDName, UTCDateTime, "
               "MessageID,"
               " Alias, EventID, BuildingSName)"
               f" VALUES('{alert['operation']}',"
               f"'{alert['message']}',"
               f"'{alert['type']}',"
               f"'{alert['bldg_disp']}','{utcdatetimenow_str}',"
               f"'{alert['message_id']}', {alias}, '{event_id}',"
               f"'{alert['building']}')")
    safe_log("Checked " + str(i + 1), "info")
    return com + ";"


def check_temp(room, alert, temps, known_issues, next_id, last_events,
               new_events):
    """Check temp."""
    if skip_alias(known_issues, alert["building"], room):
        print(room, " is decomissioned")
        return ""
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
            return ""

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
            a["message"] = angle_brackets_replace_specific(
                            a["message"], "alias",
                            room + str(" Temp"))
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
            return com + ";"
    except Exception:
        pass

    safe_log("Checked " + str(i + 1), "info")
    return ""


def check_time(data, alert, next_id, last_events, new_events):
    """Check time off since last report."""
    alias = data
    if skip_alias(known_issues, alert["building"], alias):
        print(alias, " is decomissioned")
        return ""
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
    if True:
        safe_log("An alert was sent for " + str(alert), "info")
        a = deepcopy(alert)
        a["message"] = angle_brackets_replace_specific(
                            a["message"], "alias", alias)
        a["message"] = angle_brackets_replace_specific(
                            a["message"], "days", days_since)
        event_id, next_id, new_events = assign_event_id(
                                            next_id,
                                            last_events,
                                            new_events,
                                            alert,
                                            alias)

        com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
               f"AlertMessage, Metric,BuildingDName,UTCDateTime, "
               f"MessageID, Alias, EventID, BuildingSName)"
               f" VALUES('{a['operation']}','{a['message']}',"
               f"'{a['type']}','{a['bldg_disp']}',"
               f"'{utcdatetimenow_str}',"
               f"'{alert['message_id']}', '{alias}',"
               f" '{event_id}', '{alert['building']}')")
        return com + "; "
    return ""


# Initialize logging
if LOG:
    FORMAT = '%(asctime)s %(levelname)s:%(message)s'
    datestring = str(datetime.datetime.now().date())
    log_file = os.path.join(LOGGING_PATH, datestring + '.log')
    logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)
    logging.info("NEW JOB\n---")


# Get alert conditions
alerts, unique_databases = import_conditions(alert_fname, logging)
known_issues = import_known_issues(KNOWN_ISSUES_FPATH)
occupancy = import_occupancy()

# JSON
next_id, last_events = parse_json(json_fname, json_oc, json_unoc)
new_events = {}  # id: { hash : event_id }

# Check alerts for conditions
insert_sql_total = ""
total_issues = 0
utcdatetimenow = datetime.datetime.utcnow()
utcdatetimenow_str = sql_time_str(utcdatetimenow)
for i, a in enumerate(alerts):
    alert = alerts[a]
    a_or_psid = get_alias_or_psid(alert["database"])
    try:
        # Check time conditional to make sure it is the correct time for the
        # alert
        # TODO: change this for school year
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
            all_aliases = [b[0] for b in command_to_list_multiple(z, 2)]

            for alias in all_aliases:
                try:
                    insert_sql_total += check_numerical_alias(alias, alert,
                                                              next_id,
                                                              last_events,
                                                              new_events)
                except Exception:
                    pass

        # Check each alias for temperature
        elif ("SP" in alert["value"]):
            selection_command = (f"SELECT {a_or_psid}, {alert['column']} FROM "
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
                insert_sql_total += check_temp(room, alert, temps,
                                               known_issues,
                                               next_id, last_events,
                                               new_events)

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
                safe_log("Checked " + str(i + 1), "info")
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
                insert_sql_total += check_time(data, alert, next_id,
                                               last_events, new_events)

            safe_log("Checked " + str(i + 1), "info")

        else:
            safe_log("Could not find valid condition/value for " +
                     str(alert), "info")
            print("invalid condition")

    except Exception:
        safe_log("Issue on alert " + str(i + 1) + " " + str(alert), "error")
        print("issue on alert", str(i + 1))

if insert_sql_total == "":
    insert_sql_total = ("INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType,"
                        "AlertMessage,Metric,UTCDateTime,MessageID) "
                        f"VALUES('All Clear','All Clear','N/A',"
                        f"GETUTCDATE(),'0')")

# Insert into CEVAC_ALL_ALERTS_HIST
if LOG:
    write_json_generic(new_events, next_id)
if SEND:
    f = open("/home/bmeares/cache/insert_alert_system.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/home/bmeares/scripts/exec_sql_script.sh "
              "/home/bmeares/cache/insert_alert_system.sql")
else:
    print(insert_sql_total.replace(';', '\nGO\n'))

if LOG:
    logging.info(str(datetime.datetime.now()) +
                 " TOTAL ISSUES: " + str(total_issues))
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
