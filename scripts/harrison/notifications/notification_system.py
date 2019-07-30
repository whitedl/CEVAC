"""Self notification system.

This reads from log files and checks a modification csv to notify when
something needs fixing.

To add yourself to the email list, just add name and email to `to_list`.
"""

import os
from os import system
import csv
import datetime
from jinja2 import Template
import smtplib
import ssl
from email import message as msg
import json

DEBUG = False
SEND = True

email = "cevac5733@gmail.com"
password = "cevacsteve5733"

LASR_IP = "wfic-sas-im-hd.clemson.edu"

email_fpath = ("/cevac/DEV/scripts/harrison/notifications/"
               "notification_email.html")

to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
    "Drewboi": "abemery@clemson.edu",
}


def check_plants(fname):
    """Check for all plants in log."""
    find_list = ["Central", "East", "Hinson", "West"]
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            for plant in find_list:
                if plant in line:
                    find_list.remove(plant)
    return [plant + " not found." for plant in find_list]


def check_update_time(table_name):
    """Check for last update time of table."""
    return


def ping_server(ip_address):
    """Ping an ip to test if the ip is down."""
    errors = []
    r = system(f"ping -c 2 {ip_address}")
    val = int(r)
    if val != 0:
        errors.append(f"Could not contact {ip_address}")
    return errors


def command_to_json_string(command):
    """Return a string of json from a sql command."""
    os.system("/home/bmeares/scripts/exec_sql.sh \"" + command +
              "\" temp_csv.csv")

    json_string = ""
    headers = {}
    with open("/cevac/cache/temp_csv.csv", "r") as temp_csv:
        csvfile = csv.reader(temp_csv)
        for i, row in enumerate(csvfile):
            if i == 0:
                for j, item in enumerate(row):
                    headers[j] = item
            else:
                temp_dict = {}
                try:
                    for j, item in enumerate(row):
                        temp_dict[headers[j]] = item
                    json_string += str(temp_dict)
                except Exception:
                    continue

    return json_string


def command_to_list_multiple(command, num_args):
    """Return a list of lists.

    list of lists (with length up to num_args) of data from a query.
    """
    data = command_to_json_string(command)

    data_readable = data.replace("}{", "} {").replace("\'", "\"")
    data_list = data_readable.split("} {")
    dict_list = []
    for i, d in enumerate(data_list):
        d = d if d[0] == "{" else "{" + d
        d = d if d[-1] == "}" else d + "}"
        dict_list.append(json.loads(d))

    data_list = []
    for sd in dict_list:
        try:
            dl = []
            for k in sd:
                dl.append(sd[k])
            data_list.append(dl)
        except Exception:
            pass
    return data_list


def test_tables(bldg_list, metric_list):
    """Test that tables exist."""
    errors = []
    for building in bldg_list:
        for met in metric_list:
            bldg = building.upper()
            metric = met.upper()
            command = (f"SELECT TOP 1 * FROM "
                       f"CEVAC_{bldg}_{metric}_LATEST_CACHE")
            try:
                data_list = command_to_list_multiple(command, 2)
                print(data_list)
            except Exception:
                errors.append(f"Could not access "
                              f"CEVAC_{bldg}_{metric}_LATEST_CACHE")
    return errors


def test_tables_custom(custom_list):
    """Test custom tables."""
    errors = []
    for i, table in enumerate(custom_list):
        command = f"SELECT TOP 1 * FROM {table}"
        try:
            data_list = command_to_list_multiple(command, 2)
            print(data_list)
        except Exception:
            errors.append(f"Could not access {table}")
    return errors


logs = {
    "WAP Hourly/Floor": {
        "location": "/mnt/bldg/WAP/logs/",
        "issues": [],
        "conditions": [],
        "yconditions": [],
    },
    "WAP Daily": {
        "location": "/cevac/cron/wap/log/",
        "issues": [],
        "conditions": [],
        "yconditions": [],
    },
    "Chilled Water": {
        "location": "/mnt/bldg/Campus_CHW/logs/",
        "issues": [],
        "conditions": [check_plants],
        "yconditions": [check_plants],
    },
    "Power Meters": {
        "location": "/mnt/bldg/Campus_Power/logs/",
        "issues": [],
        "conditions": [],
        "yconditions": [],
    },
    "Alert System": {
        "location": "/cevac/cron/alerts/",
        "issues": [],
        "conditions": [],
        "yconditions": [],
    },
}

custom = {
    "SAS LASR": {
        "Ping": {
            "fun": ping_server,
            "args": ["wfic-sas-im-hd.clemson.edu"],
        },
        "issues": [],
    },
    "SQL Tables": {
        "Access Tables": {
            "fun": test_tables,
            "args": [["WATT", "COOPER", "LEE_III", "ASC"],
                     ["IAQ", "TEMP", "POWER"]],
        },
        "Custom Table check": {
            "fun": test_tables_custom,
            "args": [["CEVAC_WATT_WAP_FLOOR_LATEST_CACHE"]],
        },
        "issues": [],
    }
}


def check_log(f_location, functions, logfile=None, yesterday=False):
    """Check log, return errors."""
    errors = []
    log = ""
    if logfile is None:
        now = datetime.datetime.now()
        if yesterday:
            now = now - datetime.timedelta(1)
        log = f_location + now.strftime("%Y-%m-%d") + ".log"
    else:
        log = f_location + logfile
    try:
        f = open(log, "r")
        for line in f.readlines():
            if "Error" in line:
                errors.append(line)
    except Exception:
        errors.append("Could not find log")
    for f in functions:
        errors = errors + f(log)
    return errors


def email_message(email, password, to_email, message, subject):
    """Send email."""
    port = 587
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(email, password)

        m_message = msg.Message()
        m_message.add_header('Content-Type', 'text/html')
        m_message.set_payload(message)
        m_message["Subject"] = subject
        new_message = m_message.as_string()

        print(new_message.encode("utf-8"))
        if SEND:
            server.sendmail(email, to_email, new_message.encode("utf-8"))


errors = []
for i, log in enumerate(logs):
    issues = check_log(logs[log]["location"], logs[log]["conditions"])
    print(issues)
    if len(issues) == 0:
        logs[log]["issues"].append("No issues")
    elif len(issues) > 1:
        logs[log]["issues"] += issues
    elif (issues[0] == "Could not find log"):
        issues = check_log(logs[log]["location"], logs[log]["yconditions"],
                           yesterday=True)
        if len(issues) == 0:
            logs[log]["issues"].append("No issues")
        else:
            logs[log]["issues"] += issues
    else:
        logs[log]["issues"] += issues
    print(log, logs[log]["issues"])

for i, custom_test in enumerate(custom):
    issues = []
    for some_function in custom[custom_test]:
        if some_function == "issues":
            continue
        fun = custom[custom_test][some_function]["fun"]
        args = custom[custom_test][some_function]["args"]
        issues += fun(*args)
    custom[custom_test]["issues"] += issues
    if custom[custom_test]["issues"] == []:
        custom[custom_test]["issues"] = ["No issues"]

email_msg = "".join(open(email_fpath, "r").readlines())
T = Template(email_msg)
for person in to_list:
    filled_email = T.render(logs=logs, Name=person, custom=custom)
    hr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = f"Issues at {hr_time}"
    email_message(email, password, to_list[person], filled_email, subject)

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
