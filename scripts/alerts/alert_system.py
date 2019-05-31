import os, sys
from stat import *
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
	"Alert" : 0,
	"Measure" : 1,
	"Time" : 2,
	"Date" : 3,
	"Condition" : 4,
	"Note" : 5,
}

# Definitions

def import_conditions(fname):
	alerts = {}
	with csv.reader(open(CONDITIONS_FPATH+fname)) as csvfile:
		next(csvfile)
		for row in csvfile:
			if row["condition"][0] in [">","<"]:
				alerts[row["Alert"]] = {

				}
	return alerts

def get_config(fname):
   fp = open(fname, "r")
   config = json.loads(fp.read())
   fp.close()
   return config


# Script

## Initialize logging
## *TODO*

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
	pass
