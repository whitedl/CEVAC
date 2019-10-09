"""Import WAP data from csv to sql."""

import os
import sys
from stat import S_ISREG
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

DEBUG = False
SEND = True

unique_buildings = {}

alternate_names = {
    "WFIC": "WATT",
}


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

    # The building is the third characteristic split by dashes in the
    # file name
    building_file_name = fname.split('-')[2].upper()
    if building_file_name in alternate_names:
        building_file_name = alternate_names[building_file_name]
    unique_buildings[building_file_name] = None

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
                    insert_sql_total += (f"INSERT INTO CEVAC_{building_file_name}_WAP_HIST_RAW "
                                         "(time, name, ssid, total_duration, "
                                         "predicted_occupancy, unique_users) "
                                         f"VALUES ('{hour.strftime('%Y-%m-%d %H:%M:%S')}',"
                                         f"'{name}','{SSID}','{int(total_duration)}',"
                                         f"'{total_duration/30}','{unique_users}');")
    return insert_sql_total


def ingest_file_floor(fname):
    """Use to insert by floor."""
    insert_sql_total = ""

    # The building is the third characteristic split by dashes in the
    # file name
    building_file_name = fname.split('-')[2].upper()
    if building_file_name in alternate_names:
        building_file_name = alternate_names[building_file_name]
    unique_buildings[building_file_name] = None

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
                insert_sql_total += (f"INSERT INTO  CEVAC_{building_file_name}_WAP_FLOOR_HIST_RAW "
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


def ensure_tables_procedure():
    """Make tables if they do not exist."""
    building_list = list(unique_buildings.keys())
    ensure_tables_str = ""
    for building in building_list:
        if building in alternate_names:
            building = alternate_names[building]
        test_str = ("\"SELECT TOP 1 TableName "
                    "FROM CEVAC_TABLES WHERE BuildingSName "
                    f"= '{building}' AND Metric = 'WAP'\"")
        try:
            output = os.popen("/cevac/scripts/sql_value.sh "+test_str).read()
            if output != "":
                continue
        except Exception:
            pass

        ensure_tables_str += (f"EXEC CEVAC_WAP @BuildingSName = '{building}',"
                              f" @Metric = 'WAP'\nGO\n"
                              f"EXEC CEVAC_WAP @BuildingSName = '{building}',"
                              f" @Metric = 'WAP_FLOOR'\nGO\n"
                              f"EXEC CEVAC_WAP @BuildingSName = '{building}',"
                              f" @Metric = 'WAP_DAILY'\nGO\n")
    print(ensure_tables_str)
    if SEND:
        f = open("/cevac/cache/ensure_wap_tables.sql", "w")
        f.write(ensure_tables_str)
        f.close()
        os.system("/cevac/scripts/exec_sql_script.sh "
                  "/cevac/cache/ensure_wap_tables.sql")
        os.remove("/cevac/cache/ensure_wap_tables.sql")
    return None


######################################
# Begin Script
######################################

# Check import directory for files, end program if none exist
file_list = []
for fname in os.listdir(import_dir):
    is_file = False
    if "client" in fname.lower():
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
    try:
        insert_sql_total += ingest_file_wap(fpath)
        insert_sql_total += ingest_file_floor(fpath)
        success = True
    except Exception as e:
        logging.error("Unexpected error while processing file '%s'", fpath)

    if success:
        if SEND and not DEBUG:
            try:
                safe_move(fpath, os.path.join(processed_dir, fname))
                logging.info("Successfully imported data in file " + fname)
            except WindowsError:
                logging.exception("Failed to move %s to %s.",
                                  fname, processed_dir)
    else:
        if SEND and not DEBUG:
            try:
                safe_move(fpath, os.path.join(failed_dir, fname))
            except WindowsError:
                logging.exception("Failed to move %s to %s", fname, failed_dir)

ensure_tables_procedure()
if SEND:
    f = open("/cevac/cache/insert_daily_wap3.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_daily_wap3.sql")
    os.remove("/cevac/cache/insert_daily_wap3.sql")
else:
    print(insert_sql_total.replace(";", "\nGO\n"))

# Clean output directories
cleanup()

# Close logger
logging.shutdown()
