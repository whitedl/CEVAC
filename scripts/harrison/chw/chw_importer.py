# power_importer.py

import os
import sys
from stat import *
import json
import datetime
import time
import pytz
import csv
import logging
import pandas as pd
from dateutil import tz


######################################
# Config Variables
######################################

#set up variables
prefix = "/mnt/bldg/Campus_CHW"
print(os.listdir("/mnt/bldg"))
import_dir = prefix
failed_dir = prefix
processed_dir = prefix + "/processed"
log_dir = prefix + "/logs"

SEND = True
DEBUG = False
# BTU/s
#######################################
# Function Definitions
#######################################

# convert the time strings in the wireless usage files to UTC timestamps.
# for conversion details:
# https://stackoverflow.com/questions/79797/how-do-i-convert-local-time-to-utc-in-python
def custom_datestring_to_datetime(datestring):
    dst = False
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    local = pytz.timezone ("America/New_York")
    naive = datetime.datetime.strptime(datestring, "%b %d, %Y %I:%M:%S %p")

    utc = naive.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)

    return central

def custom_datestring_utc(datestring):
    naive = datetime.datetime.strptime(datestring, "%b %d, %Y %I:%M:%S %p")
    return naive

# moves regular files and renames them if necessary. Undefined behavior if directories are passed.
def safe_move(old_path, new_path):
	try:
		os.rename(old_path, new_path)
	except WindowsError as e:
		ext = new_path.rfind('.')
		timestring = str(time.time()).replace(".", "_")
		if(ext != -1):
			new_path = new_path[0:ext] + '(' + timestring + ')' + new_path[ext:len(new_path)]
			os.rename(old_path, new_path)
		else:
			new_path = new_path + '(' + timestring + ')'
			os.rename(old_path, new_path)

# Used for the new dataset that will fail at ingest_file
def ingest_file(fname):
    errorCount = 0
    print(fname)
    name = fname.split("/")[-1].split("BTU")[0][:-1]
    print(name)

    insert_sql_total = ""
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)

        # Move reader to 'Timestamp' line
        try:
            while next(reader)[0] != 'TimeStamp':
                pass
        except StopIteration as e:
            logging.error("Couldn't find 'TimeStamp' line in %s. Unable to injest file.", fname)
            return ""

        #read past header
        headers = next(reader)

        for row in reader:
            # insert into CEVAC_ALL_CHW_RATE_HIST (BTU/sec)
            try:
                today = custom_datestring_to_datetime(row[0]).strftime('%Y-%m-%d %H:%M:%S')
                today_utc = custom_datestring_utc(row[0]).strftime('%Y-%m-%d %H:%M:%S')
                val = float(row[2].replace(",",""))
                com = "INSERT INTO  CEVAC_PLANTS_CHW_RATE_HIST_RAW (UTCDateTime, ETDateTime, Alias, ActualValue) VALUES ('"+today_utc+"','"+today+"','"+name+"','"+str(val)+"')"
                insert_sql_total += com + "; "

            except:
                errorCount += 1

            # skip if other table ended
            if len(row) < 5:
                continue

            # insert into CEVAC_ALL_CHW_HIST (kWh)
            try:
                today = custom_datestring_to_datetime(row[4]).strftime('%Y-%m-%d %H:%M:%S')
                today_utc = custom_datestring_utc(row[4]).strftime('%Y-%m-%d %H:%M:%S')
                val = float(row[6].replace(",",""))
                com = "INSERT INTO  CEVAC_PLANTS_CHW_HIST_RAW (UTCDateTime, ETDateTime, Alias, ActualValue) VALUES ('"+today_utc+"','"+today+"','"+name+"','"+str(val)+"')"
                insert_sql_total += com + "; "
            except:
                errorCount += 1

    return insert_sql_total

# remove files older than two weeks in output directories
def cleanup():
    now = time.time()
    keep_period = 1209600 # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [processed_dir, log_dir]:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if S_ISREG(os.stat(fpath).st_mode) and os.path.getatime(fpath) < cutoff:
                os.remove(fpath)

# Logging during debug
def debug_log(message, LOG):
    if LOG:
        logging.info(message)


######################################
# Begin Script
######################################

# create logger
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

# Process each file
insert_sql_total = ""
for fname in next(os.walk(import_dir))[2]:
    fpath = os.path.join(import_dir, fname)
    success = False
    try:
        insert_sql_total += ingest_file(fpath)
        success = True
    except csv.Error as e:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)
        raise

    if success:
        try:
            safe_move(fpath, os.path.join(processed_dir, fname))
            logging.info("Successfully imported data in file " + fname)
        except:
            print("not moved")

if SEND:
    #urllib.request.urlopen(command_to_query(insert_sql_total)).read()
    f = open("/home/bmeares/cache/insert_chw.sql","w")
    f.write(insert_sql_total.replace(';','\nGO\n'))
    f.close()
    os.system("/home/bmeares/scripts/exec_sql_script.sh /home/bmeares/cache/insert_chw.sql")
    os.remove("/home/bmeares/cache/insert_chw.sql")
else:
    print("DID NOT SEND")
    print(insert_sql_total.replace(';','\nGO\n'))

# clean output directories
cleanup()

# close logger
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
