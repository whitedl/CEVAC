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
	"message" : 2,
	"databse" : 3,
	"column" : 4,
	"num_entries" : 5,
	"hour" : 6,
	"day" : 7,
	"month" : 8,
	"condition" : 9,
	"value" : 10,
	"operation" : 11, 
}



# Definitions

def import_conditions(fname):
	alerts = {}
	with csv.reader(open(CONDITIONS_FPATH+fname)) as csvfile:
		next(csvfile)
		for row in csvfile:
			if row[COLUMNS["Condition"]][0] in [">","<"]:
				alerts[row["Alert"]] = {
					## TODO after regex defined
				}
	return alerts

def get_config(fname):
   fp = open(fname, "r")
   config = json.loads(fp.read())
   fp.close()
   return config

 def send_email(email_address,content):
	 ## TODO after email set up
	 pass

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

## Check alerts
for alert in alerts:
	## TODO after regex defined
	if False:
		send_email_list(emails,{})


logging.shutdown()
