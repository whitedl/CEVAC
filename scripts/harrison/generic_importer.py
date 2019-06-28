"""Generic importer for csv to sql.

Uses a logging system, safely moves old files, and cleans up directories.
"""

import os
from sys import platform
import datetime
import time
import csv
import logging
import json
from stat import S_ISREG
from dateutil import tz


######################################
# Config Variables
######################################

prefix = "/path/to/folder"
import_dir = prefix + "/import"
failed_dir = prefix + "/failed"
processed_dir = prefix + "/processed"
log_dir = prefix + "/logs"
config_file_path = prefix + "/config/dbconfig.json"

SEND = False
DEBUG = True
OS = platform

#######################################
# Function Definitions
#######################################


def custom_datestring_to_datetime(datestring):
    """Convert datestring to datetime, in UTC.

    Must be modified to fit datestring format.
    """
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    naive = datetime.datetime.strptime(datestring, "%b %d, %Y %I:%M:%S %p")

    utc = naive.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)

    return central


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


def ingest_file(fname, dbconfig=None):
    """Ingest file independent of OS."""
    if "win32" in OS:
        return ingest_file_windows(fname, dbconfig)
    elif "linux" in OS:
        return ingest_file_linux(fname)
    else:
        return None


def ingest_file_linux(fname):
    """Ingest file from csv into insertable sql, in linux."""
    error_count = 0

    insert_sql_total = ""
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)

        # Move reader to '?' line
        try:
            while next(reader)[0] != '?':
                pass
        except StopIteration:
            logging.error("Couldn't find 'TimeStamp' line in %s."
                          " Unable to injest file.", fname)
            return ""

        # Read past header
        next(reader)

        for row in reader:
            try:
                # Grab valules
                row0 = row[0]

            except Exception:
                error_count += 1
                continue

            # insert into table
            try:
                com = ("INSERT INTO  TABLE (VAR) VALUES({row0});")
                insert_sql_total += com
            except Exception:
                error_count += 1

    return insert_sql_total


def ingest_file_windows(fname, dbconfig_fname):
    """Ingest file from csv into insertable sql, in windows."""
    insert_sql_total = ""
    if SEND:
        import pypyodbc
        dbconfig = get_config(dbconfig_fname)
        try:
            connection = pypyodbc.connect(
                'Driver=' + dbconfig['driver'] + ';'
                'Server=' + dbconfig['server'] + ';'
                'Database=' + dbconfig['database'] + ';'
                'uid=' + dbconfig['uid'] + ';'
                'pwd=' + dbconfig['pwd'])
            cursor = connection.cursor()
        except Exception:
            logging.exception("Unable to connect to the database.")
            return ""

    error_count = 0

    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        insert_sql = ("INSERT INTO  TABLE (VAR) VALUES (?)")

        # Move reader to '?' line
        try:
            while reader.next()[0] != '?':
                pass
        except StopIteration:
            logging.error("Couldn't find '?' line in %s. "
                          "Unable to injest file.", fname)
            cursor.close()
            del cursor
            error_count += 1
            return ""

        # read past header
        next(reader)

        for row in reader:
            row0 = row[0]

            # Insert into database
            if SEND:
                cursor.execute(insert_sql, [row0])
            else:
                print(insert_sql, row0)
                insert_sql_total += f"{insert_sql} {row0};"

        # Commit insertions
        if SEND:
            connection.commit()

    # Close cursor
    if SEND:
        cursor.close()
        del cursor
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


def get_config(fname):
    """Get configuration from file."""
    fp = open(fname, "r")
    config = json.loads(fp.read())
    fp.close()
    return config


######################################
# Begin Script
######################################

# Create logger
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
        last_insert_sql_total = insert_sql_total
        if "win32" in OS:
            insert_sql_total += ingest_file(fpath, dbconfig=config_file_path)
            success = (insert_sql_total != last_insert_sql_total)
        elif "linux" in OS:
            insert_sql_total += ingest_file(fpath)
            success = (insert_sql_total != last_insert_sql_total)
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
            print("Not moved")

if SEND:
    if "linux" in OS:
        f = open("/home/bmeares/cache/insert_chw.sql", "w")
        f.write(insert_sql_total.replace(';', '\nGO\n'))
        f.close()
        os.system("/home/bmeares/scripts/exec_sql_script.sh "
                  "/home/bmeares/cache/insert_chw.sql")
        os.remove("/home/bmeares/cache/insert_chw.sql")
    elif "win32" in OS:
        pass
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
