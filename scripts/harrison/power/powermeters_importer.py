# power_importer.py

import os
import sys
from stat import *
import pypyodbc
import json
import datetime
import time
import pytz
import csv
import logging
import pandas as pd


######################################
# Config Variables
######################################

#set up variables
prefix = "//130.127.219.170/Watt/Watt Staff/Building/CAMPUS_POWER"
import_dir = prefix
failed_dir = prefix
processed_dir = prefix + "/processed"
log_dir = prefix + "/logs"

SEND = False
DEBUG = False

#######################################
# Function Definitions
#######################################

# convert the time strings in the wireless usage files to UTC timestamps.
# for conversion details:
# https://stackoverflow.com/questions/79797/how-do-i-convert-local-time-to-utc-in-python
def custom_datestring_to_datetime(datestring):
    return datetime.datetime.strptime(datestring, "%m/%d/%Y %I:%M:%S %p")

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

    # Turn into csv
    data_xls = pd.read_excel('fname', 'Sheet1', index_col=None)
    data_xls.to_csv('tempcsv.csv', encoding='utf-8')

    insert_sql_total = ""
    with open("tempcsv.csv", "r") as csvfile:
        reader = csv.reader(csvfile)

        # Move reader to 'Timestamp' line
        try:
            while str(next(reader)[0]) != 'Timestamp':
                 print("x")
        except StopIteration as e:
            logging.error("Couldn't find 'Timestamp' line in %s. Unable to injest file.", fname)
            return False

        #read past header
        headers = next(reader)
        for row in reader:
            try:
                today = custom_datestring_to_datetime(row[0]).strftime('%Y-%m-%d %H:%M:%S')
                kWh = float(row[1])
                com = "INSERT INTO  CEVAC_CAMPUS_ENERGY_HIST_RAW (ETDateTime, ActualValue) VALUES ('"+today+"','"+kWh+"')"
                insert_sql_total += com + "; "

            except:
                errorCount += 1

    os.remove("tempcsv.csv")

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

# check import directory for files, end program if none exist
file_list = []
for fname in os.listdir(import_dir):
    if S_ISREG(os.stat(os.path.join(import_dir, fname)).st_mode):
        file_list.append(fname)

if len(file_list) == 0:
    sys.exit()

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
            safe_move.safe_move(fpath, os.path.join(processed_dir, fname))
            logging.info("Successfully imported data in file " + fname)
        except WindowsError as e:
            logging.exception("Failed to move %s to %s.", fname, processed_dir)
    else:
        try:
            safe_move.safe_move(fpath, os.path.join(failed_dir, fname))
        except WindowsError as e:
            logging.exception("Failed to move %s to %s", fname, failed_dir)

if SEND:
    #urllib.request.urlopen(command_to_query(insert_sql_total)).read()
    f = open("/home/bmeares/cache/insert_powermeters.sql","w")
    f.write(insert_sql_total.replace(';','\nGO\n'))
    f.close()
    os.system("/home/bmeares/scripts/exec_sql_script.sh /home/bmeares/cache/insert_powermeters.sql")
    os.remove("/home/bmeares/cache/insert_powermeters.sql")
else:
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
# communicaiton, innovation, adaptability, tech, ethics
