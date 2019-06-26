# alert_system.py

"""
This CEVAC alert system script reads from alert_system.csv to populate the table
`CEVAC_ALL_ALERTS_HIST`.

TODO: Time-based alert conditionals
"""

import os
import sys
import csv
import json
import datetime
import time
import pytz
import logging
import urllib.request
import urllib.parse
from copy import deepcopy

CONDITIONS_FPATH = "/home/bmeares/cron/alerts/"
LOGGING_PATH = "/home/bmeares/cron/alerts/"
PHONE_PATH = "/home/bmeares/cron/alerts/"
alert_fname = "alert_parameters.csv"

LOG = True
DEBUG = False
CHECK_ALERTS = True
SEND = False

if DEBUG:
    CONDITIONS_FPATH = "C:\\Users\\hchall\\Downloads\\"
    LOGGING_PATH = "C:\\Users\\hchall\\Downloads\\"
    PHONE_PATH = "/home/bmeares/cron/alerts/"
    alert_fname = "Alert Parameters (working).csv"

COLUMNS = {
    "alert_name" : 0,
    "type" : 1,
    "aliases" : 2,
    "unit" : 3,
    "message" : 4,
    "building" : 5,
    "bldg_disp": 6,
    "database" : 7,
    "column" : 8,
    "sort_column" : 9,
    "num_entries" : 10,
    "time_dependent": 11,
    "occupancy_status": 12,
    "condition" : 13,
    "value" : 14,
    "operation" : 15,
    "comment": 16,
}

TIME = {
    "day" : 1,
    "hr" : 24,
    "min" : 24*60,
    "minute" : 24*60,
    "minutes" : 24*60,
}




def regex_to_numlist(regex_string):
    """
    Returns a list of numbers following expressions similar to "1-5 & 9-10" to [1,2,3,4,5,9,10]
    """
    if regex_string == "*":
            return [regex_string]
    else:
            regex_list = [([int(y)] if len(y.split("-")) == 1 else list(range(int(y.split("-")[0]),int(y.split("-")[1])+1))) for y in regex_string.replace(" ","").split("&")]
            return_list = []
            for num_list in regex_list:
                    for num in num_list:
                            return_list.append(str(num))
            return return_list


def alias_to_list(regex_string):
    """
    Returns a list of strings that were originally seperated by hyphens
    """
    if regex_string == "*":
            return ["*"]
    return regex_string.split("-")


def angle_brackets_replace(regex_string,alert):
    """
    Returns string with angle brackets replaced
    """
    lc_alert = {}
    for key in alert:
        lc_alert[key.lower()] = alert[key]
    try:
        regex_list = regex_string.replace(">","<").split("<")
        for i,regex in enumerate(regex_list):
                if regex.lower() in lc_alert:
                    regex_list[i] = lc_alert[regex]
        return "".join(regex_list)
    except:
        return regex_string


def angle_brackets_replace_single(regex_string,replacement):
    """
    Returns string with angle brackets replaced with replacement
    """
    try:
        regex_list = regex_string.replace("<","<&%").replace(">","<").split("<")
        for i,regex in enumerate(regex_list):
                if "&%" in regex:
                    regex_list[i] = replacement
        return "".join(regex_list)
    except:
        return regex_string


def import_conditions(fname,logger):
    """
    Moves CSV file to dict of alert condtions
    """
    alerts = {}
    unique_databases = {}
    with open(CONDITIONS_FPATH+fname) as csvfile:
        csvfile = csv.reader(csvfile)
        next(csvfile)
        for i,row in enumerate(csvfile):
            try:
                if (i >= 0):
                    alerts[row[COLUMNS["alert_name"]]] = {
                            "type" : row[COLUMNS["type"]],
                            "message" : row[COLUMNS["message"]],
                            "database" : row[COLUMNS["database"]],
                            "column" : row[COLUMNS["column"]],
                            "num_entries" : int(row[COLUMNS["num_entries"]]),
                            "time_dependent" : int(row[COLUMNS["time_dependent"]]),
                            "occupancy_status" : (int(row[COLUMNS["occupancy_status"]])
                                                if row[COLUMNS["occupancy_status"]] != "*" else 0),
                            "condition" : row[COLUMNS["condition"]],
                            "value" : row[COLUMNS["value"]],
                            "operation" : row[COLUMNS["operation"]],
                            "aliases" : alias_to_list(row[COLUMNS["aliases"]]),
                            "sort_column" : row[COLUMNS["sort_column"]],
                            "building" : row[COLUMNS["building"]],
                    }
                    unique_databases[row[COLUMNS["database"]]] = None
            except:
                safe_log("Issue importing conditions "+str(i),"error")
    return (alerts,unique_databases)


def command_to_query(command):
    """
    [Defunct] Returns a query-able string from a sql command
    """
    req = "http://wfic-cevac1/requests/query.php?q="
    return req + urllib.parse.quote_plus(command)


def command_to_json_string(command):
    """
    Returns a string of json from a sql command
    """
    os.system("/home/bmeares/scripts/exec_sql.sh \"" + command +
            "\" temp_csv.csv")

    json_string = ""
    headers = {}
    with open("/home/bmeares/temp_csv.csv","r") as temp_csv:
        csvfile = csv.reader(temp_csv)
        for i,row in enumerate(csvfile):
            if i == 0:
                for j,item in enumerate(row):
                    headers[j] = item
            else:
                temp_dict = {}
                for j,item in enumerate(row):
                    temp_dict[headers[j]] = item
                json_string += str(temp_dict)

    #os.remove("temp_csv.csv")
    print(json_string)
    return json_string


def command_to_list_single(command):
    """
    Returns a list of data from a query
    """
    data = command_to_json_string(command)
    data_readable = data.replace("}{","} {")
    data_list = data_readable.split("} {")
    dict_list = [json.loads(d) for d in data_list]
    data_list = [sd[list(sd.keys())[0]] for sd in dict_list]
    return data_list


def command_to_list_multiple(query, num_args):
    '''
    Returns a list of lists (with length up to num_args) of data from a query
    '''
    data = command_to_json_string(command)
    data_readable = data.replace("}{","} {")
    data_list = data_readable.split("} {")
    dict_list = []
    for i,d in enumerate(data_list):
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
        except:
            pass
    return data_list


def request_to_list_single(query):
    '''
    [Defunct] Returns a list of data from a query
    '''
    data = urllib.request.urlopen(query)
    data_readable = data.read().decode('utf-8').replace("}{","} {")
    data_list = data_readable.split("} {")
    dict_list = [json.loads(d) for d in data_list]
    data_list = [sd[list(sd.keys())[0]] for sd in dict_list]
    return data_list


def request_to_list_multiple(query, num_args):
    '''
    [Defunct] Returns a list of lists (with length up to num_args) of data from a query
    '''
    data = urllib.request.urlopen(query)
    data_readable = data.read().decode('utf-8').replace("}{","} {")
    data_list = data_readable.split("} {")
    dict_list = []
    for i,d in enumerate(data_list):
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
        except:
            pass
    return data_list


def safe_log(message,type):
    if LOG:
        if type == "error":
            logging.error(message)
        else:
            logging.info(message)




# Initialize logging
if LOG:
    FORMAT = '%(asctime)s %(levelname)s:%(message)s'
    datestring = str(datetime.datetime.now().date())
    log_file = os.path.join(LOGGING_PATH, datestring + '.log')
    logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)
    logging.info("NEW JOB\n---")


# Get alert conditions
alerts, unique_databases = import_conditions(alert_fname,logging)

# Update database cache
db_string = ""
for i,item in enumerate(list(unique_databases)):
    if i == 0:
        db_string += item + ","
    elif i == len(list(unique_databases))-1:
        db_string += item
    else:
        db_string += item + ","
update_sql = "EXEC CEVAC_CACHE_INIT @tables='" + db_string + "'"
req = "http://wfic-cevac1/requests/query.php?q="
req_parse = req + urllib.parse.quote_plus(update_sql)

append_tables_url = "http://wfic-cevac1/requests/script.php?s=append_tables.sh"

# Check alerts for conditions
insert_sql_total = ""
total_issues = 0
for i,a in enumerate(alerts):
    alert = alerts[a]
    try:
        # Check time conditional to make sure it is the correct time for the alert
        # TODO: change this for school year
        now = datetime.datetime.now()
        day = now.isoweekday()
        hour = now.hour
        correct_day = ( day >= 1 and day <= 5 )
        correct_hour = ( hour >= 8 and hour <= 5 )
        if (alert["time_dependent"]):
            if (( alert["occupancy_status"] and ((not correct_day) or (not correct_hour)) )
                or ( not alert["occupancy_status"] and ((correct_day) or (correct_hour)))):
                safe_log("Not time for alert #"+str(i+1),"info")
                continue

        # Check basic value for basic alert
        if str.isdigit(alert["value"]):
            alert["value"] = float(alert["value"])

            selection_command = (f"SELECT TOP {str(alert['num_entries'])} "
                                f"{alert['column']} FROM {str(alert['database'])}")
            if alert["aliases"] == ["*"]:
                selection_command += f" ORDER BY {alert['sort_column']} DESC"
            else:
                selection_command += (f" WHERE ALIAS IN "
                                    f"({str(alert['aliases']).replace('[','').replace(']','')})"
                                    f" ORDER BY {alert['sort_column']} DESC")

            print(selection_command)
            if not CHECK_ALERTS:
                continue

            data_list = command_to_list_single(selection_command)
            avg_data = sum(data_list)/len(data_list)

            send_alert = False
            if alert["condition"] == ">":
                send_alert = (avg_data > alert["value"])
            elif alert["condition"] == "<":
                send_alert = (avg_data < alert["value"])

            if send_alert:
                total_issues += 1
                safe_log("An alert was sent for "+str(alert),"info")
                com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
                    f"AlertMessage, Metric,BLDG,UTCDateTime)"
                    f" VALUES('{alert['operation']}','{alert['message']}',"
                    f"'{alert['type']}','{alert['building']}',GETUTCDATE())")
                insert_sql_total += com + "; "
            safe_log("Checked "+str(i+1),"info")

        # Check each alias for temperature
        elif ("Temp" in alert["value"]):
            selection_command = (f"SELECT ALIAS, {alert['column']} FROM "
                                f"{alert['database']} ORDER BY {alert['sort_column']}")
            print(selection_command)

            if not CHECK_ALERTS:
                continue

            data_list = command_to_list_multiple(selection_command,2)

            temps = {}
            ec = 0
            for row in data_list:
                try:
                    room = row[0].split()[0]
                    if room in temps:
                        temps[room][row[0][row[0].find(" ")+1:]] = float(row[1])
                    else:
                        temps[room] = {
                            row[0][row[0].find(" ")+1:] : float(row[1])
                        }
                except:
                    ec += 1

            for room in temps:
                try:
                    Alias_Temp = "Temp"
                    for key in temps[room].keys():
                        if (key != "Cooling SP" and key != "Heating SP"):
                            Alias_Temp = key

                    # Modify value
                    room_vals = temps[room]
                    try:
                        if "+" in alert["value"].split()[-1]:
                            val_str = alert["value"].split()[-1]
                            val = float(val_str[val_str.find("+")+1:])
                            room_vals["Cooling SP"] += val
                            room_val["Heating SP"] += val
                        elif "-" in alert["value"].split()[-1]:
                            val_str = alert["value"].split()[-1]
                            val = float(val_str[val_str.find("-")+1:])
                            room_vals["Cooling SP"] -= val
                            room_vals["Heating SP"] -= val
                    except:
                        pass

                    # Check value
                    send_alert = False

                    if ">" in alert["condition"]:
                        if "Cooling SP" in alert["value"]:
                            if "Cooling SP" in room_vals:
                                send_alert = (room_vals["Cooling SP"] < room_vals[Alias_Temp])
                        if "Heating SP" in alert["value"]:
                            if "Heating SP" in room_vals:
                                send_alert = (room_vals["Heating SP"] < room_vals[Alias_Temp])
                    elif "<" in alert["condition"]:
                        if "Cooling SP" in alert["value"]:
                            if "Cooling SP" in room_vals:
                                send_alert = (room_vals["Cooling SP"] > room_vals[Alias_Temp])
                        if "Heating SP" in alert["value"]:
                            if "Heating SP" in room_vals:
                                send_alert = (room_vals["Heating SP"] > room_vals[Alias_Temp])

                    if send_alert:
                        a = deepcopy(alert)
                        total_issues += 1
                        a["message"] = angle_brackets_replace_single(a["message"],room)
                        com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType,"
                            f" AlertMessage, Metric,BLDG,UTCDateTime)"
                            f" VALUES('{a['operation']}','{a['message']}',"
                            f"'{a['type']}','{a['building']}',GETUTCDATE())")
                        insert_sql_total += com + "; "
                        safe_log("An alert was sent for "+str(a),"info")
                except:
                    pass

            safe_log("Checked "+str(i+1),"info")

        # Check if aliases have reported within a given time
        elif ("<now>" in alert["value"]):
            # Find all aliases
            selection_command = "SELECT Alias FROM " + str(alert["database"])
            print(selection_command)
            if not CHECK_ALERTS:
                continue

            data_list = command_to_list_single(selection_command)
            aliases = {}
            for alias in  data_list:
                aliases[alias] = None

            # alert["value"] in format "<now> - # day/hr/min"
            dst = False
            local = pytz.timezone ("America/New_York")
            naive = datetime.datetime.now()
            local_dt = local.localize(naive, is_dst=dst)
            utc_dt = local_dt.astimezone(pytz.utc)
            try:
                amount = int(alert["value"].split()[2])
                unit_str = alert["value"].split()[3]
                unit = TIME[unit_str]
            except:
                amount = 1
                unit = TIME["hour"]
            minutes = amount * 24 / unit

            for alias in aliases:

                selection_command = (f"SELECT TOP 1 {alert['sort_column']} FROM "
                                    f"{str(alert['database'])}")
                if alert["aliases"] == ["*"]:
                    selection_command += (f" ORDER BY {alert['sort_column']} DESC"
                                        f" WHERE Alias IN ({alias})"
                                        f" ORDER BY {alert['sort_column']} DESC")
                else:
                    continue

                print(selection_command)
                data_list = command_to_list_single(selection_command)
                datetime_object = datetime.datetime.strptime(data_list[0], '%Y-%m-%d %H:%M:%S.%f')
                now_aware = pytz.utc.localize(datetime_object)
                minutes_off = (now_aware - utc_dt).total_seconds()/60

                ## Add to alerts to send
                if minutes_off > minutes:
                    total_issues += 1
                    safe_log("An alert was sent for "+str(alert),"info")
                    a = deepcopy(alert)
                    a["message"] = angle_brackets_replace_single(a["message"],alias)
                    com = (f"INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType, "
                        "AlertMessage, Metric,BLDG,UTCDateTime)"
                        f" VALUES('{a['operation']}','{a['message']}',"
                        f"'{a['type']}','{a['building']}',GETUTCDATE())")
                    insert_sql_total += com + "; "

        else:
            safe_log("Could not find valid condition/value for "+str(alert),"info")

    except:
        safe_log("Issue on alert "+str(i+1)+" "+str(alert),"info")

if total_issues == 0:
    insert_sql_total = ("INSERT INTO CEVAC_ALL_ALERTS_HIST_RAW(AlertType,"
                        "AlertMessage,Metric,BLDG,UTCDateTime) VALUES('All Clear'"
                        ",'All Clear','N/A','All',GETUTCDATE())")

# Insert into CEVAC_ALL_ALERTS_HIST
if SEND:
    f = open("/home/bmeares/cache/insert_alert_system.sql","w")
    f.write(insert_sql_total.replace(';','\nGO\n'))
    f.close()
    os.system("/home/bmeares/scripts/exec_sql_script.sh "
            "/home/bmeares/cache/insert_alert_system.sql")
    os.remove("/home/bmeares/cache/insert_alert_system.sql")
else:
    print(insert_sql_total)

if LOG:
    logging.info(str(datetime.datetime.now())+" TOTAL ISSUES: "+str(total_issues))
    logging.shutdown()
