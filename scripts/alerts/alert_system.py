import os, sys
import csv
import pypyodbc
import json
import datetime
import time
import pytz
import csv
import logging

CONDITIONS_FPATH = "C:\\Users\\hchall\\Downloads\\Alert Parameters (working).csv"
LOGGING_PATH = "C:\\Users\\hchall\\Documents\\GitHub\\CEVAC\\scripts\\alerts\\logging\\"
PHONE_PATH = "C:\\Users\\hchall\\Documents\\GitHub\\CEVAC\\scripts\\alerts\\"
CONFIG_PATH = "//130.127.219.170/Watt/Watt Staff/Building/WAP/config/"

COLUMNS = {
	"alert_name" : 0,
	"type" : 1,
	"unit" : 2,
	"message" : 3,
	"building" : 4,
	"database" : 5,
	"column" : 6,
	"sort_column" : 7,
	"num_entries" : 8,
	"hour" : 9,
	"day" : 10,
	"month" : 11,
	"condition" : 12,
	"value" : 13,
	"operation" : 14,
}



# Definitions

def regex_to_list(regex_string):
	if regex_string == "*":
		return regex_string
	else:
		regex_list = [([int(y)] if len(y.split("-")) == 1 else list(range(int(y.split("-")[0]),int(y.split("-")[1])+1))) for y in regex_string.split("&")]
		return_list = []
		for num_list in regex_list:
			for num in num_list:
				return_list.append(num)
		return return_list

def import_conditions(fname):
	alerts = {}
	with csv.reader(open(CONDITIONS_FPATH+fname)) as csvfile:
		next(csvfile)
		for i,row in enumerate(csvfile):
			try:
				if (i > 0):
					alerts[COLUMN["alert_name"]] = {
						"type" : row[COLUMNS["type"]],
						"message" : row[COLUMNS["message"]],
						"database" : row[COLUMNS["database"]],
						"column" : int(row[COLUMNS["column"]]),
						"num_entries" : int(row[COLUMNS["num_entries"]]),
						"hour" : list(range(24)) if regex_to_list(row[COLUMNS["hour"]]), #EST
						"day" : list(range(24)) if regex_to_list(row[COLUMNS["day"]]), #EST
						"month" : list(range(24)) if regex_to_list(row[COLUMNS["month"]]), #EST
						"condition" : row[COLUMNS["condition"]],
						"value" : int(row[COLUMNS["value"]]),
						"operation" : row[COLUMNS["operation"]],
					}
			except:
				pass #LOG TODO
	return alerts

def get_config(fname):
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



# Script

## Initialize logging
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(LOGGING_PATH, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

## Parse emails
fname = "phone_numbers.txt"
emails = [email.replace("\n","") for email in open(PHONE_PATH+fname)]

## Get alert conditions
fname = "Alert Parameters (Working).csv"
alerts = import_conditions(fname)

## Connect to database
fname = "dbconfig2.json"
dbconfig = get_config(CONFIG_PATH+fname)
connection = pypyodbc.connect(
	'Driver=' + dbconfig['driver'] + ';'
	'Server=' + dbconfig['server'] + ';'
	'Database=' + dbconfig['database'] + ';'
	'uid=' + dbconfig['uid'] + ';'
	'pwd=' + dbconfig['pwd'])
cursor = connection.cursor()

## Check alerts
for alert in import_conditions(CONDITIONS_FPATH):
	for i,alert in enumerate(alerts):
		try:
			now = datetime.datetime.now()
			if (now.isoweekday() in alert["day"]) and (now.hour in alert["hour"]) and (now.month in alert["month"]):
				selection_command = "SELECT top "+str(alert["num_entries"]) + " " + alerts["column"] + " FROM " + str(alerts["database"] + " ORDER BY " + alerts["sort"] + " RowNum DESC"
				data = cursor.execute(selection_command)
				data_list = [row[0] for row in data]
				avg_data = sum(data_list)/len(data_list)
				send_alert = False
				if alert["condition"] == ">":
					send_alert = (avg_data > alert["value"])
				elif alert["condition"] == "<":
					send_alert = (avg_data < alert["value"])
				if send_alert:
					## TODO check operation
					insert_sql = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertMessage,AlertType, Metric,BLDG,BeginTime)VALUES(?, ?,?,?,GETUTCDATE())"
					cursor.execute(insert_sql, [alert["message"],alert["type"],avg_data,alert["building"]])
				print("checked",alert,"\n\n")
		except:
			print("Issue on alert",i,"\n",alert,"\n\n")



logging.shutdown()
