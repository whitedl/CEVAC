"""Count all unique users in the building daily.

Run once a day at 2 AM.
"""

import os
import datetime
from datetime import datetime as dt
import csv
import logging

# Setup configuration
SEND = True
DEBUG = False

log_dir = "/cevac/cron/wap/log"
processed_dir = "/mnt/bldg/WAP/processed"

# building_file_name = "cooper"
# database_name = "CEVAC_COOPER_WAP_DAILY_HIST_RAW"
alternate_names = {
    "WFIC": "WATT",
}

CLIENT = 0
MAC = 2
SSID = 7


# Script
# Setup logging
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
datestring = str(datetime.datetime.now().date())
log_file = os.path.join(log_dir, datestring + '.log')
logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)

# Get yesterday's files
processed_files = os.listdir(processed_dir)
yesterdays_files = []
yesterday = (dt.now() - datetime.timedelta(1)).date()
for file in processed_files:
    if "client" in file:
        unix_timestamp = os.path.getmtime(processed_dir + "/" + file)
        fdate = dt.fromtimestamp(unix_timestamp).date()
        if yesterday == fdate:
            yesterdays_files.append(processed_dir + "/" + file)

# Read files into dictionary
errors = 0
databases = {}
for file in yesterdays_files:
    try:
        # The building is the third characteristic split by dashes in the
        # file name
        building_file_name = file.split('-')[2].upper()
        if building_file_name in alternate_names:
            building_file_name = alternate_names[building_file_name]
        database_name = f"CEVAC_{building_file_name}_WAP_DAILY_HIST_RAW"
        if database_name not in databases:
            databases[database_name] = {}

        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile)

            # move reader to 'Client Sessions' line
            try:
                while next(reader)[0] != 'Client Sessions':
                    pass
                next(reader)
            except StopIteration:
                logging.error("Couldn't find 'Client Sessions' line in %s. "
                              "Unable to injest file.", file)
                errors += 1
                continue

            # insert client name in dictionary
            for row in reader:
                username = row[CLIENT] if row[CLIENT] != "test" else row[MAC]
                if username != "":
                    if row[SSID] in databases[database_name]:
                        databases[database_name][row[SSID]][username] = None
                    else:
                        databases[database_name][row[SSID]] = {
                            username: None
                        }

        # DO NOT KEEP OLD FILES
        if SEND and not DEBUG:
            os.remove(file)

    except Exception:
        errors += 1
        logging.error("Could not parse file (formatting issue) " + str(file))

# Push to database
insert_sql_total = ""
for db in databases:
    network = databases[db]
    eduroam = 0 if "eduroam" not in network else len(network["eduroam"])
    clemsonguest = 0 if "clemsonguest" not in network else len(
        network["clemsonguest"])
    if DEBUG:
        print(yesterday, eduroam, clemsonguest)
        print("ERRORS:", errors)
        print("Files:", len(yesterdays_files))

    insert_sql_total += (f"INSERT INTO {db}(UTCDateTime, "
                         "clemson_count, guest_count) VALUES("
                         "'" + yesterday.strftime('%Y-%m-%d %H:%M:%S') + "',"
                         "'" + str(eduroam) + "',"
                         "'" + str(clemsonguest) + "'"
                         ")\nGO\n")

logging.info("---")
logging.info("date: " + str(yesterday))
logging.info("clemson_count: " + str(eduroam))
logging.info("guest_count: " + str(clemsonguest))

if SEND:
    f = open("/cevac/cache/insert_daily_wap2.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_daily_wap2.sql")
    os.remove("/cevac/cache/insert_daily_wap2.sql")
else:
    print(insert_sql_total)

if errors == 0:
    logging.info("Successfully inserted into daily database.")
    print("Success")
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
