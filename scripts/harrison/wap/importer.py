import os, sys
from stat import *
import pypyodbc
import json
import datetime
import time
import pytz
import csv
import logging
import safe_move
import random

######################################
# Config Variables
######################################

#set up variables
prefix = "//130.127.219.170/Watt/Watt Staff/Building/WAP"
import_dir = prefix + "/to_import"
processed_dir = prefix + "/processed"
failed_dir = prefix + "/failed"
log_dir = prefix + "/logs"
xref_dir = prefix + "/xref"

DEBUG = False

#######################################
# Function Definitions
#######################################

def get_config(fname):
   fp = open(fname, "r")
   config = json.loads(fp.read())
   fp.close()
   return config

# convert the time strings in the wireless usage files to UTC timestamps.
# for conversion details:
# https://stackoverflow.com/questions/79797/how-do-i-convert-local-time-to-utc-in-python
def custom_datestring_to_datetime(datestring):
    dst = False
    if "EDT" in datestring:
        datestring = datestring.replace("EDT", "")
        dst = True
    elif "EST" in datestring:
        datestring = datestring.replace("EST", "")
    else:
        raise ValueError('Could not recognize timezone in string "%s"' % (datestring))

    local = pytz.timezone ("America/New_York")
    naive = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
    local_dt = local.localize(naive, is_dst=dst)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt

# Convert xref to dictionary of psid to floor
def xref_to_dict(fname):
    psid_to_floor = {}

    f = open(fname,'r')
    csvreader = csv.reader(f)

    #read past header
    headers = csvreader.next()

    for row in csvreader:
        try:
            psid_to_floor[row[0]] = str(row[1])[0]
        except:
            pass

    f.close()
    return psid_to_floor


# import data from a wireless usage csv to the wireless_usage table in the database.
def ingest_file(fname, dbc):
    cursor = dbc.cursor()
    errorCount = 0

    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        insert_sql = "INSERT INTO  wireless_usage (r_id, time, assoc_count, auth_count) VALUES (?,?,?,?)"
        select_sql = "SELECT wu_key FROM wireless_usage WHERE r_id = ? AND time = ?"
        check_routers_sql = "SELECT TOP 1 r_key FROM routers WHERE name = ? AND mac = ?"
        insert_routers_sql = "INSERT INTO routers (name, mac) VALUES (?,?)"

        #move reader to 'Client Count' line
        try:
            while reader.next()[0] != 'Client Count':
                pass
        except StopIteration as e:
            logging.error("Couldn't find 'Client Count' line in %s. Unable to injest file.", fname)
            cursor.close()
            del cursor
            return False

        #read past header
        headers = reader.next()

        # dictionary for remembering query results
        routerDict = {}

        # keep track of duplicate entries
        dupCount = 0

        for row in reader:
            #validate row length, don't count empty rows as errors
            if len(row) != 5:
                if len(row) != 0 and row[0] != ' ':
                    logging.error("Row is not a valid length. File: %s, line: %s.", fname, reader.line_num)
                    errorCount += 1
                continue

            routerName = row[0]
            routerMac = row[1]
            r_id = None

            if routerDict.has_key(routerName + "/" + routerMac):
                r_id = routerDict.get(routerName + "/" + routerMac)
            else:
                # get r_id from routers table, creating row if necessary
                cursor.execute(check_routers_sql, (routerName, routerMac))
                r_row = cursor.fetchone()
                if not r_row:
                    cursor.execute(insert_routers_sql, (routerName, routerMac))
                    cursor.execute(check_routers_sql, (routerName, routerMac))
                    r_row = cursor.fetchone()
                r_id = r_row['r_key']
                routerDict[routerName + "/" + routerMac] = r_id

            #parse string to timestamp
            time = None
            try:
                time = custom_datestring_to_datetime(row[2])
            except ValueError as e:
                logging.error("Value Error in converting string to timestamp. File: %s, line: %s.", fname, reader.line_num)
                errorCount += 1
                continue

            #check to see if data is already in db. Don't add duplicate rows. Don't count duplicates as errors.
            cursor.execute(select_sql, [r_id, time])
            matched_row = cursor.fetchone()
            if matched_row:
                dupCount = dupCount + 1
                continue

            #insert data
            cursor.execute(insert_sql, [r_id, time, row[3], row[4]])

        #commit insertions
        dbc.commit()

        #log duplicates Warning
        if(dupCount > 0):
            logging.warning("In %s, found %d entries that are already in the database.", fname, dupCount)

    # close cursor
    cursor.close()
    del cursor
    return errorCount == 0

# Used for the new dataset that will fail at ingest_file
def ingest_file_fail(fname, dbc):
    cursor = dbc.cursor()
    errorCount = 0

    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        insert_sql = "INSERT INTO  CEVAC_WATT_WAP_HIST_RAW (time, name, ssid, total_duration, predicted_occupancy, unique_users) VALUES (?,?,?,?,?,?)"

        #move reader to 'Client Sessions' line
        try:
            while reader.next()[0] != 'Client Sessions':
                pass
        except StopIteration as e:
            logging.error("Couldn't find 'Client Sessions' line in %s. Unable to injest file.", fname)
            cursor.close()
            del cursor
            return False

        #read past header
        headers = next(reader)

        hours = {}
        for row in reader:
            name = row[5]
            username = row[0]
            if username == "test":
                username = str(random.randint(0,10000000))
            SSID = row[7]
            hour = custom_datestring_to_datetime(row[3]).replace(minute=0,second=0)
            assoc_time = custom_datestring_to_datetime(row[3])
            try:
                dissoc_time = custom_datestring_to_datetime(row[10])
            except:
                dst = False
                local = pytz.timezone ("America/New_York")
                dissoc_time = datetime.datetime.now()
                dissoc_time = local.localize(dissoc_time, is_dst=dst)
                dissoc_time = dissoc_time.astimezone (pytz.utc)
            snr_db = row[11]
            rssi_dbm = row[12]
            td = ((dissoc_time - assoc_time).total_seconds()/60) % 60

            ## Add count of unique people per wap
            if (hour in hours.keys()) and (td > 1):
                if name in hours[hour].keys():
                    if SSID in hours[hour][name].keys():
                        hours[hour][name][SSID]["time"] += td
                        hours[hour][name][SSID]["users"][username] = None
                    else:
                        hours[hour][name][SSID] = {
                            "time" : td,
                            "users" : {
                                username : None,
                            }
                        }
                else:
                    hours[hour][name] = {
                        SSID : {
                            "time" : td,
                            "users" : {
                                username : None,
                            }
                        }
                    }
            elif (td > 1):
                hours[hour] = {
                    name : {
                        SSID : {
                            "time": td,
                            "users" : {
                                username : None,
                            }
                        }
                    }
                }

        for hour in hours:
            for name in hours[hour]:
                for SSID in hours[hour][name]:
                    total_duration = hours[hour][name][SSID]["time"]
                    unique_users = len(hours[hour][name][SSID]["users"].keys())
                    cursor.execute(insert_sql, [hour, name, SSID, int(total_duration), total_duration/60, unique_users])

        #commit insertions
        dbc.commit()


    # close cursor
    cursor.close()
    del cursor
    return errorCount == 0

# Used to insert by floor
def ingest_file_floor(fname, dbc, xref):
    cursor = dbc.cursor()
    errorCount = 0

    logging.info("opening file")
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        insert_sql = "INSERT INTO  CEVAC_WATT_WAP_FLOOR_HIST (UTCDateTime, floor, guest_count, clemson_count) VALUES (?,?,?,?)"
        #move reader to 'Client Sessions' line
        try:
            while reader.next()[0] != 'Client Sessions':
                pass
        except StopIteration as e:
            logging.error("Couldn't find 'Client Sessions' line in %s. Unable to injest file.", fname)
            cursor.close()
            del cursor
            return False

        #read past header
        headers = next(reader)
        hours = {}
        for row in reader:
            try:
                name = row[5]
                vendor = row[4]

                # Filter bad vendors
                if vendor in ["Oculus VR, LLC"]:
                    continue

                if name in xref:
                    floor = xref[name]
                else:
                    floor = "outside"
                username = row[0]
                if username == "test":
                    username = str(random.randint(0,10000000))
                SSID = row[7]
                hour = custom_datestring_to_datetime(row[3]).replace(minute=0,second=0)
                assoc_time = custom_datestring_to_datetime(row[3])
                try:
                    dissoc_time = custom_datestring_to_datetime(row[10])
                except:
                    dst = False
                    local = pytz.timezone ("America/New_York")
                    dissoc_time = datetime.datetime.now()
                    dissoc_time = local.localize(dissoc_time, is_dst=dst)
                    dissoc_time = dissoc_time.astimezone (pytz.utc)
                snr_db = row[11]
                rssi_dbm = row[12]
                td = ((dissoc_time - assoc_time).total_seconds()/60) % 60

                ## Add count of unique people per wap
                #debug_log("okay",LOG)
                if (hour in hours.keys()) and (td > 1):
                    #debug_log("hour in  keys",LOG)
                    if floor in hours[hour].keys():
                        if SSID in hours[hour][floor].keys():
                            hours[hour][floor][SSID]["time"] += td
                            hours[hour][floor][SSID]["users"][username] = None
                        else:
                            hours[hour][floor][SSID] = {
                                "time" : td,
                                "users" : {
                                    username : None,
                                }
                            }
                    else:
                        hours[hour][floor] = {
                            SSID : {
                                "time" : td,
                                "users" : {
                                    username : None,
                                }
                            }
                        }
                elif (td > 1):
                    #debug_log("here",LOG)
                    hours[hour] = {
                        floor : {
                            SSID : {
                                "time": td,
                                "users" : {
                                    username : None,
                                }
                            }
                        }
                    }
                #debug_log("success insert",LOG)
            except:
                logging.error("router not in xref")

        for hour in hours:
            for floor in hours[hour]:
                clemson = 0
                guest = 0
                if "eduroam" in hours[hour][floor]:
                    clemson += len(hours[hour][floor]["eduroam"]["users"])
                if "clemsonguest" in hours[hour][floor]:
                    guest += len(hours[hour][floor]["clemsonguest"]["users"])

                cursor.execute(insert_sql, [hour, floor, guest, clemson])

        #commit insertions
        dbc.commit()


    # close cursor
    cursor.close()
    del cursor
    return errorCount == 0

# remove files older than two weeks in output directories
def cleanup():
    now = time.time()
    keep_period = 1209600 # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [processed_dir, failed_dir, log_dir]:
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


# Load DB config file
if(not len(sys.argv) == 2):
   logging.exception("No config file specified. Please specify the config file: python get_forecast.py <config_file_path>")
   logging.shutdown()
   exit()
dbconfig_file = sys.argv[1]
try:
    dbconfig = get_config(dbconfig_file)
    dbconfig2 = get_config("//130.127.219.170/Watt/Watt Staff/Building/WAP/config/dbconfig2.json")
except IOError as ioe:
    logging.exception("Unable to locate database config file.")
    logging.shutdown()
    raise

# Establish DB connection
logging.info("Connecting to first database")
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

# Process each file
for fname in file_list:
    fpath = os.path.join(import_dir, fname)
    success = False
    try:
        success = ingest_file(fpath, connection)
    except csv.Error as e:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)
        logging.error(e.message)
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

# close db connection
connection.close()

# Connect to second database
logging.info("Connecting to CEVAC_WATT_WAP_HIST and CEVAC_WATT_WAP_HIST_FLOOR")

file_list = []
try:
    for fname in os.listdir(failed_dir):
        if S_ISREG(os.stat(os.path.join(failed_dir, fname)).st_mode):
            file_list.append(fname)
except:
    logging.info("Issue extracting failed_dir names")


if len(file_list) == 0:
    logging.info("No files in failed_dir")
    logging.shutdown()
    sys.exit()

# Establish DB connection
try:
    connection = pypyodbc.connect(
        'Driver=' + dbconfig2['driver'] + ';'
        'Server=' + dbconfig2['server'] + ';'
        'Database=' + dbconfig2['database'] + ';'
        'uid=' + dbconfig2['uid'] + ';'
        'pwd=' + dbconfig2['pwd'])
except pypyodbc.Error as dbe:
    logging.exception("Unable to connect to the database.")
    logging.info("Issue with connection")
    logging.shutdown()
    raise

# Process each file
for fname in file_list:
    fpath = os.path.join(failed_dir, fname)
    success = False
    logging.info("Running for "+str(fpath))
    try:
        logging.info("starting xref")
        xref = xref_to_dict(os.path.join(xref_dir, "CEVAC_WATT_WAP_XREF.csv"))
        logging.info("Finished xref")
        if len(xref) > 0:
            logging.info("xref > 0")
            success_a = ingest_file_fail(fpath, connection)
            logging.info("success_b")
            success_b = ingest_file_floor(fpath,connection,xref)
            success = (success_a and success_b)
            logging.info("Passed both")
        else:
            success = ingest_file_fail(fpath, connection)
            logging.error("Unable to read xref, append to CEVAC_WATT_WAP_HIST_FLOOR")
    except csv.Error as e:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)
        logging.error(e.message)
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


connection.close()

# clean output directories
cleanup()

# close logger
logging.shutdown()
