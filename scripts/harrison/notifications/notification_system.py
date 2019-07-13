"""Self notification system.

This reads from log files and checks a modification csv to notify when
something needs fixing.

To add yourself to the email list, just add name and email to `to_list`.
"""

import datetime
from jinja2 import Template
import smtplib
import ssl
from email import message as msg

DEBUG = False
SEND = True

email = "cevac5733@gmail.com"
password = "cevacsteve5733"

email_fpath = ("/cevac/DEV/scripts/harrison/notifications/"
               "notification_email.html")

to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
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

email_msg = "".join(open(email_fpath, "r").readlines())
T = Template(email_msg)
for person in to_list:
    filled_email = T.render(logs=logs, Name=person)
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
