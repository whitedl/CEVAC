# daily_count.py
# Run once a day at 2 AM

import os
import sys
import pypyodbc
import json
import datetime
from datetime import datetime as dt
import time
import pytz
import csv
import logging

# Setup configuration
prefix = "//130.127.219.170/Watt/Watt Staff/Building/WAP"
import_dir = prefix + "/to_import"
processed_dir = prefix + "/processed"
failed_dir = prefix + "/failed"
log_dir = prefix + "/logs"

CLIENT = 0
SSID = 7


def get_config(fname):
   fp = open(fname, "r")
   config = json.loads(fp.read())
   fp.close()
   return config


# Script
## Setup logging
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

## Connect to database
dbconfig = get_config("//130.127.219.170/Watt/Watt Staff/Building/WAP/config/dbconfig2.json")
try:
	connection = pypyodbc.connect(
		'Driver=' + dbconfig['driver'] + ';'
		'Server=' + dbconfig['server'] + ';'
		'Database=' + dbconfig['database'] + ';'
		'uid=' + dbconfig['uid'] + ';'
		'pwd=' + dbconfig['pwd'])
except pypyodbc.Error as dbe:
	logging.exception("Unable to connect to the database.")
	logging.shutdown()
	raise

## Get yesterday's files
processed_files = os.listdir(processed_dir)
yesterdays_files = []
yesterday = (dt.now() - datetime.timedelta(1)).date()
for file in processed_files:
	if "client" in file:
		unix_timestamp = os.path.getmtime(processed_dir+"/"+file)
		fdate = dt.fromtimestamp(unix_timestamp).date()
		if yesterday == fdate:
			yesterdays_files.append(processed_dir+"/"+file)

## Read files into dictionary
errors = 0
network = {}
for file in yesterdays_files:
	try:
		with open(file, "r") as csvfile:
			reader = csv.reader(csvfile)

			#move reader to 'Client Sessions' line
			try:
				while next(reader)[0] != 'Client Sessions':
					pass
				next(reader)
			except StopIteration as e:
				logging.error("Couldn't find 'Client Sessions' line in %s. Unable to injest file.", fname)
				errors += 1
				continue

			# insert client name in dictionary
			for row in reader:
				if row[CLIENT] != "":
					if row[SSID] in network:
						network[row[SSID]][row[CLIENT]] = None
					else:
						network[row[SSID]] = {
							row[CLIENT] : None
						}

	except:
		errors += 1
		logging.error("Could not parse file "+str(file))

# Push to database
eduroam = 0 if "eduroam" not in network else len(network["eduroam"])
clemsonguest = 0 if "clemsonguest" not in network else len(network["clemsonguest"])
#print(yesterday,eduroam,clemsonguest)

cursor = connection.cursor()
cursor.execute("INSERT INTO CEVAC_WATT_WAP_DAILY(Hour, Clemson, Guest) VALUES(?,?,?)",[yesterday, eduroam, clemsonguest])
cursor.commit()

cursor.close()
connection.close()

if errors == 0:
	logging.info("Successfully inserted into daily database")
logging.shutdown()
