"""Import WAP data from csv to sql using pypyodbc."""

import os
import sys
from stat import S_ISREG
import json
import datetime
import time
import pytz
import csv
import logging

######################################
# Config Variables
######################################

prefix = "/mnt/bldg/WAP"
import_dir = prefix + "/to_import"
processed_dir = prefix + "/processed"
failed_dir = prefix + "/failed"
log_dir = prefix + "/logs"
xref_dir = prefix + "/xref"

wap_table = "CEVAC_COOPER_WAP_HIST_RAW"
floor_table = "CEVAC_COOPER_WAP_FLOOR_HIST_RAW"
building_file_name = "cooper"

DEBUG = False
SEND = True


#######################################
# Function Definitions
#######################################
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


def custom_datestring_to_datetime(datestring):
    """Convert the time strings in the wireless usage files to UTC timestamps.

    for conversion details:
    https://stackoverflow.com/questions/79797/how-do-i-convert-local-time-to-utc-in-python
    """
    dst = False
    if "EDT" in datestring:
        datestring = datestring.replace("EDT", "")
        dst = True
    elif "EST" in datestring:
        datestring = datestring.replace("EST", "")
    else:
        raise ValueError('Could not recognize timezone in string "%s"' %
                         (datestring))

    local = pytz.timezone("America/New_York")
    naive = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
    local_dt = local.localize(naive, is_dst=dst)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def xref_to_dict(fname):
    """Convert xref to dictionary of psid to floor."""
    psid_to_floor = {}

    f = open(fname, 'r')
    csvreader = csv.reader(f)

    # read past header
    csvreader.next()

    for row in csvreader:
        try:
            psid_to_floor[row[0]] = str(row[1])[0]
        except Exception:
            pass

    f.close()
    return psid_to_floor


def ingest_file_wap(fname):
    """Use for the new dataset that will fail at ingest_file."""

    insert_sql_total = ""
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)

        # Move reader to 'Client Sessions' line
        try:
            while next(reader)[0] != 'Client Sessions':
                pass
        except StopIteration:
            return ""

        # read past header
        next(reader)

        hours = {}
        for row in reader:
            name = row[5]
            username = row[0]
            if username == "test":
                username = row[2]
            SSID = row[7]
            hour = custom_datestring_to_datetime(row[3])
            if hour.minute < 30:
                hour = hour.replace(minute=0, second=0)
            else:
                hour = hour.replace(minute=30, second=0)
            assoc_time = custom_datestring_to_datetime(row[3])
            try:
                dissoc_time = custom_datestring_to_datetime(row[10])
            except Exception:
                dst = False
                local = pytz.timezone("America/New_York")
                dissoc_time = datetime.datetime.now()
                dissoc_time = local.localize(dissoc_time, is_dst=dst)
                dissoc_time = dissoc_time.astimezone(pytz.utc)
            snr_db = row[11]
            rssi_dbm = row[12]
            td = ((dissoc_time - assoc_time).total_seconds() / 60) % 60

            # Add count of unique people per wap
            if (hour in hours.keys()) and (td > 1):
                if name in hours[hour].keys():
                    if SSID in hours[hour][name].keys():
                        hours[hour][name][SSID]["time"] += td
                        hours[hour][name][SSID]["users"][username] = None
                    else:
                        hours[hour][name][SSID] = {
                            "time": td,
                            "users": {
                                username: None,
                            }
                        }
                else:
                    hours[hour][name] = {
                        SSID: {
                            "time": td,
                            "users": {
                                username: None,
                            }
                        }
                    }
            elif (td > 1):
                hours[hour] = {
                    name: {
                        SSID: {
                            "time": td,
                            "users": {
                                username: None,
                            }
                        }
                    }
                }
        for hour in hours:
            for name in hours[hour]:
                for SSID in hours[hour][name]:
                    total_duration = hours[hour][name][SSID]["time"]
                    unique_users = len(hours[hour][name][SSID]["users"].keys())
                    insert_sql_total += (f"INSERT INTO  {wap_table} "
                                         "(time, name, ssid, total_duration, "
                                         "predicted_occupancy, unique_users) "
                                         f"VALUES ('{hour.strftime('%Y-%m-%d %H:%M:%S')}',"
                                         f"'{name}','{SSID}','{int(total_duration)}',"
                                         f"'{total_duration/30}','{unique_users}');")
    return insert_sql_total


def ingest_file_floor(fname):
    """Use to insert by floor."""
    insert_sql_total = ""
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        # Move reader to 'Client Sessions' line
        try:
            while next(reader)[0] != 'Client Sessions':
                pass
        except StopIteration:
            return ""

        # Read past header
        next(reader)
        hours = {}
        insert_sql_total = ""
        for row in reader:
            try:
                name = row[5]
                vendor = row[4]

                # Filter bad vendors
                if vendor in ["Oculus VR, LLC"]:
                    continue

                floor = name.split("-")[2]
                username = row[0]
                if username == "test":
                    username = row[2]
                SSID = row[7]
                hour = custom_datestring_to_datetime(row[3])
                if hour.minute < 30:
                    hour = hour.replace(minute=0, second=0)
                else:
                    hour = hour.replace(minute=30, second=0)
                assoc_time = custom_datestring_to_datetime(row[3])
                try:
                    dissoc_time = custom_datestring_to_datetime(row[10])
                except Exception:
                    dst = False
                    local = pytz.timezone("America/New_York")
                    dissoc_time = datetime.datetime.now()
                    dissoc_time = local.localize(dissoc_time, is_dst=dst)
                    dissoc_time = dissoc_time.astimezone(pytz.utc)
                snr_db = row[11]
                rssi_dbm = row[12]
                td = ((dissoc_time - assoc_time).total_seconds() / 60) % 60
                # Add count of unique people per wap
                if (hour in hours.keys()) and (td > 1):
                    if floor in hours[hour].keys():
                        if SSID in hours[hour][floor].keys():
                            hours[hour][floor][SSID]["time"] += td
                            hours[hour][floor][SSID]["users"][username] = None
                        else:
                            hours[hour][floor][SSID] = {
                                "time": td,
                                "users": {
                                    username: None,
                                }
                            }
                    else:
                        hours[hour][floor] = {
                            SSID: {
                                "time": td,
                                "users": {
                                    username: None,
                                }
                            }
                        }
                elif (td > 1):
                    hours[hour] = {
                        floor: {
                            SSID: {
                                "time": td,
                                "users": {
                                    username: None,
                                }
                            }
                        }
                    }
            except Exception:
                pass
        for hour in hours:
            for floor in hours[hour]:
                clemson = 0
                guest = 0
                if "eduroam" in hours[hour][floor]:
                    clemson += len(hours[hour][floor]["eduroam"]["users"])
                if "clemsonguest" in hours[hour][floor]:
                    guest += len(hours[hour][floor]["clemsonguest"]["users"])
                insert_sql_total += (f"INSERT INTO  {floor_table} "
                                     "(UTCDateTime, floor, guest_count, clemson_count) "
                                     f"VALUES ('{hour.strftime('%Y-%m-%d %H:%M:%S')}',"
                                     f"'{floor}','{guest}','{clemson}');")
    return insert_sql_total


def cleanup():
    """Remove files older than two weeks in output directories."""
    now = time.time()
    keep_period = 1209600  # 1209600 seconds == two weeks
    cutoff = now - keep_period

    for directory in [processed_dir, failed_dir, log_dir]:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if (S_ISREG(os.stat(fpath).st_mode) and
                    os.path.getatime(fpath) < cutoff):
                os.remove(fpath)


def debug_log(message, LOG):
    """Log during debug."""
    if LOG:
        logging.info(message)


######################################
# Begin Script
######################################

# Check import directory for files, end program if none exist
file_list = []
for fname in os.listdir(import_dir):
    is_file = False
    if building_file_name in fname.lower():
        is_file = True
    if not is_file:
        continue
    if S_ISREG(os.stat(os.path.join(import_dir, fname)).st_mode):
        file_list.append(fname)

if len(file_list) == 0:
    sys.exit()

# Create logger
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)


# Process each file
insert_sql_total = ""
for fname in file_list:
    fpath = os.path.join(import_dir, fname)
    success = False
    logging.info("Running for " + str(fpath))
    try:
        insert_sql_total += ingest_file_wap(fpath)
        insert_sql_total += ingest_file_floor(fpath)
        success = True
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)
        #logging.error(e.message)

    if success:
        if SEND and not DEBUG:
            try:
                safe_move(fpath, os.path.join(processed_dir, fname))
                logging.info("Successfully imported data in file " + fname)
            except WindowsError:
                logging.exception("Failed to move %s to %s.", fname, processed_dir)
    else:
        if SEND and not DEBUG:
            try:
                safe_move(fpath, os.path.join(failed_dir, fname))
            except WindowsError:
                logging.exception("Failed to move %s to %s", fname, failed_dir)


if SEND:
    f = open("/cevac/cache/insert_daily_wap3.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_daily_wap3.sql")
    os.remove("/cevac/cache/insert_daily_wap3.sql")
else:
    print(insert_sql_total.replace(";","\nGO\n"))

# Clean output directories
cleanup()

# Close logger
logging.shutdown()
