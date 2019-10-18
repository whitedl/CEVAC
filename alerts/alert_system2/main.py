"""CEVAC Alert System alert_system.py.

Main script for CEVAC alert sytem.
"""

from tools import string_to_bool, verbose_print
import alerts
import email
import ml

import datetime
import argparse
import os

# Parse arguments
parser = argparse.ArgumentParser(description='Parse ')
parser.add_argument("--log", "-L", "-l", default=True, action="store",
                    help="Set log to True or False")
parser.add_argument("--alerts", "-a", "-A", default=False, action="store_true",
                    help="Check alerts currently.")
parser.add_argument("--times", "-t", "-T", default=0, action="store",
                    help=("If set, checks alerts for different time periods "
                          "where possible"))
parser.add_argument("--send", "-s", "-S", default=False, action="store_true",
                    help="Send anomalies to our database.")
parser.add_argument("--email", "-e", "-E", default=False, action="store_true",
                    help="Send email of anomalies.")
parser.add_argument("--emailtime", "-et", "-ET", default=24, action="store",
                    help=("Set hours of anomalies to send via email. "
                          "[Default=24]"))
parser.add_argument("--cache", "-c", "-C", default=False, action="store_true",
                    help="Update the cache before checking alerts.")
parser.add_argument("--machinelearning", "-ml", "-ML", default=False,
                    action="store_true",
                    help=("Run machine learning algorithm after checking "
                          "alerts."))
parser.add_argument("--verbose", "-v", "-V", default=False,
                    action="store_true", help="Determines printing.")


parsed_args = parser.parse_args()

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

# Determines whether or not to run the ML algorithm
RUN_ML = parsed_args.machinelearning

# Printing boolean
VERBOSE = parsed_args.verbose

if __name__ == "__main__":
    verbose_print(VERBOSE, f"Job Started: {datetime.datetime.now()} ET")

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

    if UPDATE_CACHE:
        alerts.update_cache()
        verbose_print(VERBOSE, "UPDATE_CACHE is True")

    all_alerts = None
    if CHECK_ALERTS:
        all_alerts = alerts.Alerts()
        all_alerts.alert_system()
        verbose_print(VERBOSE, "CHECK_ALERTS is True")

    if SEND:
        if all_alerts is not None:
            all_alerts.send()
        verbose_print(VERBOSE, "SEND is True")

    if SEND_EMAIL:
        email_setup = email.Email(hours=EMAIL_TIME, verbose=VERBOSE)
        email_setup.send()
        verbose_print(VERBOSE, "EMAIL is True")

    if RUN_ML:
        machine_learning = ml.ML()
        if CHECK_ALERTS:
            machine_learning.add_nodes(all_alerts)
            machine_learning.send()
        machine_learning.queries()
        verbose_print(VERBOSE, "ML is True")

    # Finish system
    print("Ran successfully.")
    verbose_print(VERBOSE, f"Job Completed: {datetime.datetime.now()} ET")
