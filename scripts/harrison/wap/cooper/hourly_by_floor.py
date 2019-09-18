import sys
from stat import *
import pypyodbc
import json
import datetime
import time
import pytz
import csv
import logging
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


# Used to insert by floor
def ingest_file_floor(fname, dbc):
    cursor = dbc.cursor()
    errorCount = 0

    logging.info("opening file")
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        insert_sql = "INSERT INTO CEVAC_COOPER_WAP_FLOOR_HIST (UTCDateTime, floor, guest_count, clemson_count) VALUES (?,?,?,?)"
        #move reader to 'Client Sessions' line
        try:
            while next(reader)[0] != 'Client Sessions':
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
                if (hour in hours.keys()) and (td > 1):
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
            except:
                logging.error(f"WAP name ({name}) not in xref")

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

# create logger
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)


# Load DB config file
try:
    dbconfig2 = get_config("//130.127.219.170/Watt/Watt Staff/Building/WAP/config/dbconfig2.json")
except IOError as ioe:
    logging.exception("Unable to locate database config file.")
    logging.shutdown()
    raise

# Connect to second database
file_list = []
try:
    for fname in os.listdir(processed_dir):
        if "cooper" not in fname.lower():
            continue
        if S_ISREG(os.stat(os.path.join(processed_dir, fname)).st_mode):
            file_list.append(fname)
except:
    logging.info("Issue extracting processed_dir names")


if len(file_list) == 0:
    logging.info("No cooper files in processed_dir")
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
    logging.shutdown()
    raise

# Process each file
for fname in file_list:
    fpath = os.path.join(processed_dir, fname)
    success = False
    try:
        if True:
            success = ingest_file_floor(fpath, connection)
        else:
            # success = ingest_file_fail(fpath, connection)
            logging.error("Unable to append to CEVAC_WATT_WAP_HIST_FLOOR")
    except csv.Error as e:
        logging.error("Failed to read %s as a csv file.", fpath)
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)
        raise


connection.close()

# clean output directories
cleanup()

# close logger
logging.shutdown()
