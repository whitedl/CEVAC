# daily_count.py
# Run once a day at 2 AM

import os
import sys
import json
import datetime
from datetime import datetime as dt
import time
import pytz
import csv
import logging
import urllib.request
import urllib.parse
import random

# Setup configuration
SEND = True
DEBUG = False

log_dir = "/home/bmeares/cron/wap/log"
processed_dir = "/mnt/bldg/WAP/processed"
if DEBUG:
    log_dir = "C:\\Users\\hchall\\Downloads"
    processed_dir = "//130.127.219.170/Watt/Watt Staff/Building/WAP/processed"

CLIENT = 0
SSID = 7


def command_to_query(command):
    """
    Returns a query-able string from a sql command
    """
    req = "http://wfic-cevac1/requests/query.php?q="
    return req + urllib.parse.quote_plus(command)


# Script
## Setup logging
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

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
                username = row[CLIENT] if row[CLIENT] != "test" else str(random.randint(0,100000000))
                if username != "":
                    if row[SSID] in network:
                        network[row[SSID]][username] = None
                    else:
                        network[row[SSID]] = {
                            username : None
                        }

    except:
        errors += 1
        logging.error("Could not parse file "+str(file))

# Push to database
eduroam = 0 if "eduroam" not in network else len(network["eduroam"])
clemsonguest = 0 if "clemsonguest" not in network else len(network["clemsonguest"])
if DEBUG:
    print(yesterday,eduroam,clemsonguest)
    print("ERRORS:",errors)
    print("Files:",len(yesterdays_files))

insert_sql_total = ("INSERT INTO CEVAC_WATT_WAP_DAILY_HIST(UTCDateTime, clemson_count, guest_count) VALUES("
                    "'"+yesterday.strftime('%Y-%m-%d %H:%M:%S')+"',"
                    "'"+str(eduroam)+"',"
                    "'"+str(clemsonguest)+"'"
                    ");")

logging.info("---")
logging.info("date: " + str(yesterday))
logging.info("clemson_count: " + str(eduroam))
logging.info("guest_count: " + str(clemsonguest))

if SEND:
    urllib.request.urlopen(command_to_query(insert_sql_total)).read()
else:
    print(insert_sql_total,"\n",command_to_query(insert_sql_total))

if errors == 0:
    logging.info("Successfully inserted into daily database")
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
