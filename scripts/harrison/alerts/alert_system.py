# alert_system.py

### TODO: angle bracket replation, time-based alert conditionals
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

CONDITIONS_FPATH = "/home/bmeares/cron/alerts/"
LOGGING_PATH = "/home/bmeares/cron/alerts/"
PHONE_PATH = "/home/bmeares/cron/alerts/"
CONFIG_PATH = "/home/bmeares/cron/alerts/"

LOG = True

COLUMNS = {
        "alert_name" : 0,
        "type" : 1,
        "aliases" : 2,
        "unit" : 3,
        "message" : 4,
        "building" : 5,
        "database" : 6,
        "column" : 7,
        "sort_column" : 8,
        "num_entries" : 9,
        "hour" : 10,
        "day" : 11,
        "month" : 12,
        "condition" : 13,
        "value" : 14,
        "operation" : 15,
}



# Definitions

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
    TODO
    """
    try:
        regex_list = regex_string.replace("<","").split(">")
        for regex in regex_list:
                if regex == "asdf":
                        #TODO
                        pass
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
                            "hour" : regex_to_numlist(row[COLUMNS["hour"]]), #EST
                            "day" : regex_to_numlist(row[COLUMNS["day"]]), #EST
                            "month" : regex_to_numlist(row[COLUMNS["month"]]), #EST
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


def get_config(fname):
    """
    Returns json of database connection configuration file
    """
    fp = open(fname, "r")
    config = json.loads(fp.read())
    fp.close()
    return config


def command_to_query(command):
    """
    Returns a query-able string from a sql command
    """
    req = "http://wfic-cevac1/requests/query.php?q="
    return req + urllib.parse.quote_plus(command)


def request_to_list_single(query):
    '''
    Returns a list of data from a query
    '''
    data = urllib.request.urlopen(query)
    data_readable = data.read().decode('utf-8').replace("}{","} {")
    data_list = data_readable.split(" ")
    dict_list = [json.loads(d) for d in data_list]
    data_list = [sd[list(sd.keys())[0]] for sd in dict_list]
    return data_list


def request_to_list_multiple(query, num_args):
    '''
    Returns a list of lists (with length up to num_args) of data from a query
    '''
    data = urllib.request.urlopen(query)
    data_readable = data.read().decode('utf-8').replace("}{","} {")
    data_list = data_readable.split(" ")
    dict_list = [json.loads(d) for d in data_list]
    data_list = []
    for sd in dict_list:
        dl = []
        for i in range(num_args):
            dl.append(sd[list[sd.keys()]][i])
        data_list.append(ds)
    return data_list


def safe_log(message,type):
    if LOG:
        if type == "error":
            logging.error(message)
        else:
            logging.info(message)

# Script

## Initialize logging
if LOG:
    FORMAT = '%(asctime)s %(levelname)s:%(message)s'
    datestring = str(datetime.datetime.now().date())
    log_file = os.path.join(LOGGING_PATH, datestring + '.log')
    logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)
    logging.info("NEW JOB\n---")


## Get alert conditions
fname = "alert_parameters.csv"
alerts, unique_databases = import_conditions(fname,logging)

## Update database cache
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
urllib.request.urlopen(append_tables_url).read()

## Check alerts
insert_sql_total = ""
total_issues = 0
for i,a in enumerate(alerts):
    alert = alerts[a]
    insert_sql = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES(?,?,?,?,GETUTCDATE())"
    try:
        # Check time conditional
        now = datetime.datetime.now()
        correct_day = ( (str(now.isoweekday()) in alert["day"]) or (alert["day"] == ["*"]) )
        correct_hour = ( (str(now.hour) in alert["hour"]) or (alert["hour"] == ["*"]) )
        correct_month = ( (str(now.month) in alert["month"]) or (alert["month"] == ["*"]) )
        if not correct_day or not correct_hour or not correct_month:
            safe_log("Not time for alert #"+str(i+1),"info")
            continue

        # Check basic value
        if str.isdigit(alert["value"]):
            alert["value"] = float(alert["value"])

            selection_command = "SELECT top "+str(alert["num_entries"]) + " " + alert["column"] + " FROM " + str(alert["database"])
            if alert["aliases"] == ["*"]:
                selection_command += " ORDER BY " + alert["sort_column"] + " DESC"
            else:
                selection_command += " WHERE " + "Alias" + " IN (" + str(alert["aliases"]).replace("[","").replace("]","") + ") ORDER BY " + alert["sort_column"] + " DESC"

            data_list = command_to_query(command_to_query(selection_command))
            avg_data = sum(data_list)/len(data_list)

            send_alert = False
            if alert["condition"] == ">":
                send_alert = (avg_data > alert["value"])
            elif alert["condition"] == "<":
                send_alert = (avg_data < alert["value"])
            if send_alert:
                total_issues += 1
                safe_log("An alert was sent for "+str(alert),"info")
                com = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES('"+alert["operation"]+"','"+alert["message"]+"','"+str(avg_data)+"','"+alert["building"]+"',GETUTCDATE())"
                insert_sql_total += com + "; "
                "ISSUE"+str(alert)
            safe_log("Checked "+str(i+1),"info")

        # Temperature custom measure
        elif ("Temp" in alert["value"]):
            selection_command = "SELECT Alias, " + alert["column"] + " FROM " + alert["database"] + " ORDER BY " + alert["sort_column"]
            url_command = command_to_query(selection_command)
            data = urllib.request.urlopen(url_command)
            print(data)
            data_readable = data.read().decode('utf-8').replace("}{","} {")
            data_list = data_readable.split(" ")
            print(data_list)
            dict_list = [json.loads(d) for d in data_list]
            data_list = [[sd[list(sd.keys())[0]],sd[list(sd.keys())[1]]] for sd in dict_list]
            print(data_list)

            #data_list = [[row[0],row[1]] for row in data]
            temps = {}
            for row in data_list:
                room = row[0].split()[0]
                if room in temps:
                    temps[room][row[0][row[0].find(" ")+1:]] = float(row[1])
                else:
                    temps[room] = {
                        row[0][row[0].find(" ")+1:] : float(row[1])
                    }

            for room in temps:
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
                    total_issues += 1
                    com = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES('"+alert["operation"]+"','"+alert["message"]+"','"+str(room) + " " + str(room_vals[Alias_Temp])+"','"+alert["building"]+"',GETUTCDATE())"
                    insert_sql_total += com + "; "
                    safe_log("An alert was sent for "+str(alert),"info")
                safe_log("Checked "+str(i+1),"info")

        # Time custom measure
        elif ("<now>" in alert["value"]):
            #local_dt = local.localize(naive, is_dst=None)
            #utc_dt = local_dt.astimezone(pytz.utc)
            safe_log("<now> not yet ready in script","info")

        else:
            safe_log("Could not find valid condition/value for "+str(alert),"info")

    except:
        safe_log("Issue on alert "+str(i+1)+" "+str(alert),"info")

if total_issues == 0:
    insert_sql_total = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType,AlertMessage,Metric,BLDG,BeginTime) VALUES('All Clear','All Clear','N/A','All',GETUTCDATE())"

# Insert into CEVAC_WATT_ALERT_HIST
urllib.request.urlopen(command_to_query(insert_sql_total)).read()

if LOG:
    logging.info(str(datetime.datetime.now())+" TOTAL ISSUES: "+str(total_issues))
    logging.shutdown()
