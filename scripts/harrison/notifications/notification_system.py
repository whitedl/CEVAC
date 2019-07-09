"""Self notification system.

This reads from log files and checks a modification csv to notify when
something needs fixing.
"""

import os
import sys
import csv
import json
import datetime
import pytz
import logging
import urllib.request
from copy import deepcopy

DEBUG = False
CHECK_ALERTS = True
SEND = False

logs = {
    "WAP Hourly/Floor": "",
    "WAP Daily": "",
    "Chilled Water": "/mnt/bldg/Campus_CHW/logs/",
    "Power Meters": "/mnt/bldg/Campus_Power/logs/",
}


def check_log(f_location, logfile=None):
    """Check log, return errors."""
    errors = []
    if logfile is None:
        now = datetime.datetime.now()
        log = f_location + now.strftime("%Y-%m-%d") + ".log"
    else:
        log = f_location + logfile
    print(logfile)
    try:
        f = open(log, "r")
        for line in f.readlines():
            if "Error" in line:
                print(line)
                errors.append(line)
    except Exception:
        errors.append("Could not find log")
    return errors

for i, log in enumerate(logs):
    pass


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
