# alert_system.py

### TODO: special

import os, sys
import csv
import pypyodbc
import json
import datetime
import time
import pytz
import csv
import logging

CONDITIONS_FPATH = "C:\\Users\\hchall\\Downloads\\"
LOGGING_PATH = "C:\\Users\\hchall\\Documents\\GitHub\\CEVAC\\scripts\\alerts\\logging\\"
PHONE_PATH = "C:\\Users\\hchall\\Documents\\GitHub\\CEVAC\\scripts\\alerts\\"
CONFIG_PATH = "//130.127.219.170/Watt/Watt Staff/Building/WAP/config/"

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
			if regex == "" #TODO
	except:
		return regex_string


def import_conditions(fname,logger):
	alerts = {}
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
						"value" : float(row[COLUMNS["value"]]),
						"operation" : row[COLUMNS["operation"]],
						"aliases" : alias_to_list(row[COLUMNS["aliases"]]),
						"sort_column" : row[COLUMNS["sort_column"]],
					}
			except:
				logger.error("Issue importing conditions "+str(i))
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
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(LOGGING_PATH, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

## Parse emails
fname = "phone_numbers.txt"
emails = [email.replace("\n","") for email in open(PHONE_PATH+fname)]

## Get alert conditions
fname = "Alert Parameters (Working).csv"
alerts = import_conditions(fname,logging)

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
for i,a in enumerate(alerts):
	alert = alerts[a]
	try:
		now = datetime.datetime.now()
		if (((str(now.isoweekday()) in alert["day"]) or (str(alert["day"]) == "*"))
		and ((str(now.hour) in alert["hour"]) or (str(alert["hour"]) == "*"))
		and ((str(now.month) in alert["month"]) or (str(alert["month"]) == "*"))):
			selection_command = "SELECT top "+str(alert["num_entries"]) + " " + alert["column"] + " FROM " + str(alert["database"])
			if str(alert["aliases"]) == "*":
				selection_command += " ORDER BY " + alert["sort_column"] + " DESC"
			else:
				selection_command += " WHERE " + "Alias" + " IN (" + str(alert["aliases"]).replace("[","").replace("]","") + ") ORDER BY " + alert["sort_column"] + " DESC"
			data = cursor.execute(selection_command)
			data_list = [row[0] for row in data]
			avg_data = sum(data_list)/len(data_list)
			send_alert = False
			if alert["condition"] == ">":
				send_alert = (avg_data > alert["value"])
			elif alert["condition"] == "<":
				send_alert = (avg_data < alert["value"])
			if send_alert:
				insert_sql = "INSERT INTO CEVAC_ALL_ALERTS_HIST(AlertMessage,AlertType, Metric,BLDG,BeginTime) VALUES(?,?,?,?,GETUTCDATE())"
				cursor.execute(insert_sql, [alert["message"],alert["operation"],avg_data,alert["building"]])
				logging.info("An alert was sent for "+str(alert))
			logging.info("Checked "+str(alert))
		else:
			#print("Not time for",alert)
			pass
	except:
		logging.error("Issue on alert "+str(i)+" "+str(alert))


logging.shutdown()
