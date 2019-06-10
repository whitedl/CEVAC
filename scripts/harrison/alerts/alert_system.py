# alert_system.py

### TODO: angle bracket replation, time-based alert conditionals
import urllib.parse
import os
import sys
import csv
#import pypyodbc
import json
import datetime
import time
import pytz
import logging
import urllib.request

CONDITIONS_FPATH = "/home/bmeares/cron/alerts/"
LOGGING_PATH = "/home/bmeares/cron/alerts/"
PHONE_PATH = "/home/bmeares/cron/alerts/"
CONFIG_PATH = "/home/bmeares/cron/alerts/"

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
                return regex_string
        else:
                regex_list = [([int(y)] if len(y.split("-")) == 1 else list(range(int(y.split("-")[0]),int(y.split("-")[1])+1))) for y in regex_string.replace(" ","").split("&")]
                return_list = []
                for num_list in regex_list:
                        for num in num_list:
                                return_list.append(num)
                return return_list


def alias_to_list(regex_string):
        """
        Returns a list of strings that were originally seperated by hyphens
        """
        if regex_string == "*":
                return "*"
        return regex_string.split("-")


def angle_brackets_replace(regex_string,alert):
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
                                logger.error("Issue importing conditions "+str(i))
        return (alerts,unique_databases)


def get_config(fname):
        """
        Returns json of database connection configuration file
        """
        fp = open(fname, "r")
        config = json.loads(fp.read())
        fp.close()
        return config


def send_email(email_address,content):
        ## TODO after email set up
        return


def send_email_list(email_address_list,content):
        for email_address in email_address_list:
                send_email(email_address,content)

def command_to_query(command):
        req = "http://wfic-cevac1/requests/query.php?q="
        return req + urllib.parse.quote_plus(command)

# Script

## Initialize logging
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(LOGGING_PATH, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)
logging.info("NEW JOB\n---")

## Parse emails
#  fname = "phone_numbers.txt"
#  emails = [email.replace("\n","") for email in open(PHONE_PATH+fname)]

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
#  print(update_sql)
#  print(req_parse)

#  na = urllib.request.urlopen(req+update_sql.replace(" ","%20")).read()
append_tables_url = 'http://wfic-cevac1/requests/script.php?s=append_tables.sh';
print(append_tables_url)
na = urllib.request.urlopen(append_tables_url).read()

#cursor.execute(update_sql)
#cursor.commit()

## Check alerts
insert_sql_total = ""
total_issues = 0
for i,a in enumerate(alerts):
        alert = alerts[a]
        insert_sql = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES(?,?,?,?,GETUTCDATE())"
        try:
                now = datetime.datetime.now()
                if (((str(now.isoweekday()) in alert["day"]) or (str(alert["day"]) == "*"))
                and ((str(now.hour) in alert["hour"]) or (str(alert["hour"]) == "*"))
                and ((str(now.month) in alert["month"]) or (str(alert["month"]) == "*"))):
                        # Check basic value
                        if str.isdigit(alert["value"]):
                                alert["value"] = float(alert["value"])
                                print(type(alert["value"]))

                                selection_command = "SELECT top "+str(alert["num_entries"]) + " " + alert["column"] + " FROM " + str(alert["database"])
                                print(selection_command)
                                if str(alert["aliases"]) == "*":
                                        selection_command += " ORDER BY " + alert["sort_column"] + " DESC"
                                else:
                                        selection_command += " WHERE " + "Alias" + " IN (" + str(alert["aliases"]).replace("[","").replace("]","") + ") ORDER BY " + alert["sort_column"] + " DESC"
                                #data = cursor.execute(selection_command)
                                url_command = command_to_query(selection_command)
                                print(url_command)
                                data = urllib.request.urlopen(command_to_query(selection_command))
                                print(data)
                                data2 = data.read()
                                print(data2)
                                data2 = data2.decode('utf-8')
                                data3 = data2.replace("}{","} {")
                                print(data3)
                                data4 = data3.split(" ")
                                print(data4)
                                dict_list = [json.loads(d) for d in data4]
                                print(dict_list)
                                data_list = [sd[list(sd.keys())[0]] for sd in dict_list]
                                print(data_list)

                                #data_list = [row[0] for row in data]
                                avg_data = sum(data_list)/len(data_list)
                                send_alert = False
                                if alert["condition"] == ">":
                                        send_alert = (avg_data > alert["value"])
                                elif alert["condition"] == "<":
                                        send_alert = (avg_data < alert["value"])
                                if send_alert:
                                        total_issues += 1
                                        logging.info("ISSUE"+str(alert))
                                        com = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES('"+alert["operation"]+"','"+alert["message"]+"','"+str(avg_data)+"','"+alert["building"]+"',GETUTCDATE())"
                                        insert_sql_total += com + "; "
                                        logging.info("An alert was sent for "+str(alert))
                                logging.info("Checked "+str(alert))

                        # Temperature custom measure
                        elif ("Temp" in alert["value"]):
                                selection_command = "SELECT Alias, " + alert["column"] + " FROM " + alert["database"] + " ORDER BY " + alert["sort_column"]
                                #data = cursor.execute(selection_command)
                                url_command = command_to_query(selection_command)
                                print(selection_command)
                                print(url_command)
                                data = urllib.request.urlopen(command_to_query(selection_command)).read().replace("}{","} {").split(" ")
                                dict_list = [json.loads(d) for d in data]
                                data_list = [[sd[list(sd.keys())[0]],sd[list(sd.keys())[1]]] for sd in dict_list]

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
                                                logging.info("ISSUE"+str(alert))
                                                com = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType, AlertMessage, Metric,BLDG,BeginTime) VALUES('"+alert["operation"]+"','"+alert["message"]+"','"+str(room) + " " + str(room_vals[Alias_Temp])+"','"+alert["building"]+"',GETUTCDATE())"
                                                insert_sql_total += com + "; "
                                                logging.info("An alert was sent for "+str(alert))
                                        logging.info("Checked "+str(alert))

                        # Time custom measure
                        elif ("<now>" in alert["value"]):
                                #local_dt = local.localize(naive, is_dst=None)
                                #utc_dt = local_dt.astimezone(pytz.utc)
                                logging.error("<now> not yet ready in script")

                        else:
                                logging.error("Could not find valid condition/value for "+str(alert))
                else:
                        logging.info(alert["alert_name"]+"Not time")
        except:
                logging.error("Issue on alert "+str(i)+" "+str(alert))

if total_issues == 0:
        insert_sql = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertType,Metric,BLDG,BeginTime) VALUES('All Clear','','All',GETUTCDATE())"
        pass

#print(insert_sql_total)
#cursor.execute(insert_sql_total)
urllib.request.urlopen(command_to_query(insert_sql_total)).read()

logging.info(str(datetime.datetime.now())+" TOTAL ISSUES: "+str(total_issues))
logging.shutdown()
