"""Import power meter data as xls."""

import os
import sys
from stat import S_ISREG
import datetime
import time
import csv
import logging
import pandas as pd


######################################
# Config Variables
######################################

# set up variables
prefix = "/mnt/bldg/CAMPUS_POWER"
print(os.listdir("/mnt/bldg"))
import_dir = prefix
failed_dir = prefix
processed_dir = prefix + "/processed"
log_dir = prefix + "/logs"

SEND = True
DEBUG = False

#######################################
# Function Definitions
#######################################


def custom_datestring_to_datetime(datestring):
    """Return DateTime object of datestring."""
    return datetime.datetime.strptime(datestring, "%m/%d/%Y %I:%M:%S %p")


def safe_move(old_path, new_path):
    """Safely move files."""
    try:
        os.rename(old_path, new_path)
    except WindowsError:
        ext = new_path.rfind('.')
        timestring = str(time.time()).replace(".", "_")
        if(ext != -1):
            new_path = new_path[0:ext] + \
                '(' + timestring + ')' + new_path[ext:len(new_path)]
            os.rename(old_path, new_path)
        else:
            new_path = new_path + '(' + timestring + ')'
            os.rename(old_path, new_path)


def ingest_file(fname):
    """Ingest file into insertable sql code."""
    errorCount = 0

    # Turn into csv
    data_xls = pd.read_excel(fname, 'Sheet1', index_col=None)
    data_xls.to_csv('tempcsv.csv', encoding='utf-8')

    insert_sql_total = ""
    with open("tempcsv.csv", "r") as csvfile:
        reader = csv.reader(csvfile)

        header = {}
        skip = True
        for row in reader:
            if skip:
                if row[1] == "Timestamp":
                    for i, col in enumerate(row):
                        header[i] = col.split(" ")[0]
                    skip = False
                else:
                    continue
            try:
                today = custom_datestring_to_datetime(
                    row[1]).strftime('%Y-%m-%d %H:%M:%S')
                for i, col in enumerate(row):
                    try:
                        kWh = float(row[i])
                        com = ("INSERT INTO  CEVAC_CAMPUS_ENERGY_HIST_RAW " +
                               "(ETDateTime, Alias, ActualValue) VALUES ('" +
                               today + "','" + header[i] + "','" + str(kWh)
                               + "')")
                        insert_sql_total += com + "; "
                    except Exception:
                        continue

            except Exception:
                errorCount += 1

    os.remove("tempcsv.csv")

    return insert_sql_total


def cleanup():
    """Safely remove file older than 2 weeks."""
    now = time.time()
    keep_period = 1209600  # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [processed_dir, log_dir]:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if (S_ISREG(os.stat(fpath).st_mode)
                    and os.path.getatime(fpath) < cutoff):
                os.remove(fpath)


def debug_log(message, LOG):
    """Safely log messages."""
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
    except csv.Error:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception:
        logging.error("Unexpected error while processing file '%s'", fpath)
        raise

    if success and SEND:
        try:
            safe_move(fpath, os.path.join(processed_dir, fname))
            logging.info("Successfully imported data in file " + fname)
        except Exception:
            print("not moved")

if SEND:
    # urllib.request.urlopen(command_to_query(insert_sql_total)).read()
    f = open("/cevac/cache/insert_powermeters.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_powermeters.sql")
    os.remove("/cevac/cache/insert_powermeters.sql")
    cleanup()
else:
    print("DID NOT SEND")
    print(insert_sql_total.replace(';', '\nGO\n'))

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
