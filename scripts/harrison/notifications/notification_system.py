"""Self notification system.

This reads from log files and checks a modification csv to notify when
something needs fixing.
"""

import datetime
from jinja2 import Template
import smtplib
import ssl
from email import message as msg

DEBUG = False
CHECK_ALERTS = True
SEND = True

email = "cevac5733@gmail.com"
password = "cevacsteve5733"

to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
}

logs = {
    "WAP Hourly/Floor": {
        "location": "/mnt/bldg/WAP/logs/",
        "issues": [],
    },
    "WAP Daily": {
        "location": "/cevac/cron/wap/log/",
        "issues": [],
    },
    "Chilled Water": {
        "location": "/mnt/bldg/Campus_CHW/logs/",
        "issues": [],
    },
    "Power Meters": {
        "location": "/mnt/bldg/Campus_Power/logs/",
        "issues": [],
    },
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


def email_message(email, password, to_email, message, subject):
    """Send email."""
    port = 587
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    # message = message.replace("\n", "<br>")
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
        server.sendmail(email, to_email, new_message)


errors = []
for i, log in enumerate(logs):
    issues = check_log(logs[log]["location"])
    if len(issues) != 0:
        logs[log]["issues"] += issues
    else:
        logs[log]["issues"].append("No issues")

email = "".join(open("notification_email.html", "r").readlines())
T = Template(email)
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
