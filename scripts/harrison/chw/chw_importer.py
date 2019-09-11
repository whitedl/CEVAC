"""Import chilled water data."""

import os
import datetime
import time
import csv
import logging
from stat import S_ISREG
from dateutil import tz


######################################
# Config Variables
######################################

prefix = "/mnt/bldg/Campus_CHW"
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

# convert the time strings in the wireless usage files to UTC timestamps.
# for conversion details:
# https://stackoverflow.com/questions/79797/how-do-i-convert-local-time-to-utc-in-python


def custom_datestring_to_datetime(datestring):
    """Convert UTC to EST."""
    to_zone = tz.gettz('UTC')
    from_zone = tz.gettz('America/New_York')
    naive = datetime.datetime.strptime(datestring, "%b %d, %Y %I:%M:%S %p")

    utc = naive.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)

    return central


def custom_datestring_utc(datestring):
    """Convert datestring to datetime object."""
    naive = datetime.datetime.strptime(datestring, "%b %d, %Y %I:%M:%S %p")
    return naive


def safe_move(old_path, new_path):
    """Move files safely."""
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
    """Ingest file from csv into insertable sql."""
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
        except StopIteration:
            logging.error("Couldn't find 'TimeStamp' line in %s."
                          " Unable to injest file.", fname)
            return ""

        # read past header
        next(reader)

        for row in reader:
            # insert into CEVAC_ALL_CHW_RATE_HIST (BTU/sec)
            try:
                today = custom_datestring_to_datetime(
                    row[0]).strftime('%Y-%m-%d %H:%M:%S')
                today_utc = custom_datestring_utc(
                    row[0]).strftime('%Y-%m-%d %H:%M:%S')
                val = float(row[2].replace(",", ""))
                com = ("INSERT INTO  CEVAC_PLANTS_CHW_RATE_HIST_RAW "
                       "(UTCDateTime, ETDateTime, Alias, ActualValue) "
                       "VALUES ('" + today_utc + "','" + today + "','" +
                       name + "','" + str(val) + "')")
                insert_sql_total += com + "; "

            except Exception:
                errorCount += 1

            # skip if other table ended
            if len(row) < 5:
                continue

            # insert into CEVAC_ALL_CHW_HIST (kWh)
            try:
                today_utc = custom_datestring_to_datetime(
                    row[4]).strftime('%Y-%m-%d %H:%M:%S')
                today = custom_datestring_utc(
                    row[4]).strftime('%Y-%m-%d %H:%M:%S')
                val = float(row[6].replace(",", ""))
                com = ("INSERT INTO  CEVAC_PLANTS_CHW_HIST_RAW (UTCDateTime, "
                       "ETDateTime, Alias, ActualValue) VALUES ('" +
                       today_utc + "','" + today + "','" +
                       name + "','" + str(val) + "')")
                insert_sql_total += com + "; "
            except Exception:
                errorCount += 1

    return insert_sql_total


def cleanup():
    """Remove files older than 2 weeks."""
    now = time.time()
    keep_period = 1209600  # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [processed_dir, log_dir]:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if (S_ISREG(os.stat(fpath).st_mode) and
                    os.path.getatime(fpath) < cutoff):
                os.remove(fpath)


def debug_log(message, LOG):
    """Safely log files."""
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
    except csv.Error:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception:
        logging.error("Unexpected error while processing file '%s'", fpath)
        raise

    if success:
        try:
            safe_move(fpath, os.path.join(processed_dir, fname))
            logging.info("Successfully imported data in file " + fname)
        except Exception:
            print("not moved")

if SEND:
    f = open("/cevac/cache/insert_chw.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_chw.sql")
    os.remove("/cevac/cache/insert_chw.sql")
else:
    print("DID NOT SEND")
    print(insert_sql_total.replace(';', '\nGO\n'))

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
