"""CEVAC Alert System alert_system.py.

Main script for CEVAC alert sytem.
"""

import tools
import alerts

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
                    help="If set, checks alerts for different time periods where possible")
parser.add_argument("--send", "-s", "-S", default=False, action="store_true",
                    help="Send anomalies to our database.")
parser.add_argument("--email", "-e", "-E", default=False, action="store_true",
                    help="Send email of anomalies.")
parser.add_argument("--emailtime", "-et", "-ET", default=24, action="store",
                    help="Set hours of anomalies to send via email. [Default=24]")
parser.add_argument("--cache", "-c", "-C", default=False, action="store_true",
                    help="Update the cache before checking alerts.")
parser.add_argument("--machinelearning", "-ml", "-ML", default=False, action="store_true",
                    help="Run machine learning algorithm after checking alerts.")


parsed_args = parser.parse_args()

# Determines whether or not to write a log and keep track of event id's
LOG = tools.string_to_bool(parsed_args.log)
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

if __name__ == "__main__":
    print(f"Job Started: {datetime.datetime.now()} EST")

    logging = None
    if LOG:
        import logging
        print("LOG is True")
        FORMAT = "%(asctime)s %(levelname)s:%(message)s"
        datestring = str(datetime.datetime.now().date())
        log_file = os.path.join(LOGGING_PATH, datestring + ".log")
        logging.basicConfig(filename=log_file, format=FORMAT,
                            level=logging.INFO)
        logging.info("\n---\nNEW JOB\n---")
    print(f"logging: {logging}")

    if UPDATE_CACHE:
        alerts.update_cache()
        print("UPDATE_CACHE is True")

    all_alerts = None
    if CHECK_ALERTS:
        all_alerts = alerts.Alerts()
        all_alerts.alert_system()
        print("CHECK_ALERTS is True")

    if SEND:
        if all_alerts != None:
            all_alerts.send()
        print("SEND is True")

    if SEND_EMAIL:
        print("EMAIL is True")

    if RUN_ML:
        print("ML is True")

    # Finish system
    print("Ran successfully.")
