"""CEVAC Alert System alert_system.py.

Main script for CEVAC alert sytem.
"""

from tools.tools import string_to_bool, verbose_print
from alerts import alerts
from emails import email_handler
from machine_learning import ml

import datetime
import argparse
import os
import pyodbc

# Parse arguments
parser = argparse.ArgumentParser(
    description=(
        "Alert System v2. "
        "This alert system is heavily modular, "
        "allowing options to be passed "
        "via the command line, as opposed to being "
        "burried in scripts."
    )
)
parser.add_argument(
    "--debug", "-D", "-d",
    default=False, action="store_true",
    help="Runs script in debug where possible."
)
parser.add_argument(
    "--log", "-L", "-l",
    default=True, action="store",
    help="set log to True or False"
)
parser.add_argument(
    "--alerts", "-a", "-A",
    default=False, action="store_true",
    help="check alerts currently"
)
parser.add_argument(
    "--times", "-t", "-T",
    default=0, action="store",
    help=(
        "if set, checks alerts for different "
        "time periods where possible"
    )
)
parser.add_argument(
    "--send", "-s", "-S",
    default=False, action="store_true",
    help="send anomalies to our database"
)
parser.add_argument(
    "--email", "-e", "-E",
    default=False, action="store_true",
    help="send email of anomalies"
)
parser.add_argument(
    "--web", "-w", "-W",
    default=False, action="store_true",
    help=(
        "update email as web page "
        "(wfic-cevac1/cevac_alerts/alerts.html)"
    )
)
parser.add_argument(
    "--emailtime", "-et", "-ET",
    default=24, action="store",
    help=(
        "set hours of anomalies to send via email"
        "[Default=24]"
    )
)
parser.add_argument(
    "--cache", "-c", "-C",
    default=False, action="store_true",
    help="update the cache before checking alerts"
)
parser.add_argument(
    "--machinelearning", "-ml", "-ML",
    default=False, action="store_true",
    help=(
        "run machine learning algorithm after "
        "checking alerts"
    )
)

parser.add_argument(
    "--queue", "-q", "-Q",
    default=False, action="store_true",
    help=(
        "read queue for alerts instead of all alerts"
    )
)

parser.add_argument(
    "--verbose", "-v", "-V",
    default=False,
    action="store_true", help="printing"
)


parsed_args = parser.parse_args()

# DEBUG argument
DEBUG = parsed_args.debug

# Determines whether or not to write a log and keep track of event id's
LOG = string_to_bool(parsed_args.log)
LOGGING_PATH = "/cevac/cron/alerts/"

# Determines whether or not to check the alerts against the respectful
# databases
CHECK_ALERTS = parsed_args.alerts

# Determines whether or not to insert the found alerts into the alert database
SEND = parsed_args.send

# Determines whether or not to update the cache alerts are checked against
UPDATE_CACHE = parsed_args.cache

# Determines whether or not to send emails
SEND_EMAIL = parsed_args.email
EMAIL_TIME = parsed_args.emailtime

# Determines whether or not to update the html page
UPDATE_WEB = parsed_args.web

# Determines whether or not to run the ML algorithm
RUN_ML = parsed_args.machinelearning

# Determines whether or not to use queue
RUN_QUEUE = parsed_args.queue

# Printing boolean
VERBOSE = parsed_args.verbose

if __name__ == "__main__":
    verbose_print(
        VERBOSE,
        f"Job Started: {datetime.datetime.now()} ET"
    )

    logging = None
    if LOG:
        import logging
        FORMAT = "%(asctime)s %(levelname)s:%(message)s"
        datestring = str(datetime.datetime.now().date())
        log_file = os.path.join(LOGGING_PATH, datestring + ".log")
        logging.basicConfig(filename=log_file, format=FORMAT,
                            level=logging.INFO)
        logging.info("\n---\nNEW JOB\n---")
    verbose_print(VERBOSE, f"logging: {logging}")

    conn = None
    if CHECK_ALERTS or SEND_EMAIL or RUN_ML:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=130.127.218.11;"
            "DATABASE=WFIC-CEVAC;"
            "UID=wficcm;"
            "PWD=5wattcevacmaint$"
        )

    all_alerts = None
    if CHECK_ALERTS or RUN_QUEUE:
        all_alerts = alerts.Alerts(logging, UPDATE_CACHE,
                                   verbose=VERBOSE, conn=conn,
                                   queue=RUN_QUEUE
        )
        all_alerts.alert_system()
        verbose_print(VERBOSE, "CHECK_ALERTS is True")
        verbose_print(VERBOSE,(
            f"Anomalies: {len(all_alerts.anomalies)}\n"
            f"{all_alerts.num_decom_anomalies()} "
            "anomalies are decommissioned"
        ))

    if SEND:
        if all_alerts is not None:
            all_alerts.send()
        verbose_print(VERBOSE, "SEND is True")

    if RUN_QUEUE and SEND:
        while len(all_alerts.get_queue_buildings()) > 0:
            all_alerts = alerts.Alerts(
                logging, UPDATE_CACHE,
                verbose=VERBOSE, conn=conn,
                queue=RUN_QUEUE
            )
            all_alerts.alert_system()
            all_alerts.send()

    if SEND_EMAIL or UPDATE_WEB:
        email_setup = email_handler.Email(
            hours=EMAIL_TIME,
            verbose=VERBOSE,
            conn=conn
        )
        if SEND_EMAIL:
            email_setup.send(debug=DEBUG)
        if UPDATE_WEB:
            email_setup.write_to_file()
        verbose_print(VERBOSE, "EMAIL is True")

    if RUN_ML:
        if CHECK_ALERTS:
            machine_learning = ml.ML(
                all_alerts.anomalies,
                conn=conn,
                verbose=VERBOSE
            )
            machine_learning.do_ml()
            if SEND:
                machine_learning.send()
        else:
            print("CHECK_ALERTS REQUIRED FOR ML")
        verbose_print(VERBOSE, "ML is True")

    # Finish system
    print("Ran successfully.")
    verbose_print(
        VERBOSE,
        f"Job Completed: {datetime.datetime.now()} ET"
    )

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
