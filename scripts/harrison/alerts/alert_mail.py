"""Parse alerts from CEVAC_ALL_ALERTS_HIST."""

import bsql
import datetime
import time_handler
import smtplib
import ssl
from jinja2 import Template


email = "cevac5733@gmail.com"
password = "cevacsteve5733"
to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
    # "Bennett Meares": "bmeares@g.clemson.edu"
}
f = open("alert_email.html", "r")
page = Template("".join(f.readlines()))


def email_message(email, password, to_list, message, subject):
    """Send email."""
    print("here")
    port = 587
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(email, password)
        print(email, subject, "\n", message)
        for person in to_list:
            email = to_list[person]
            p_page = Template.render(Name=email)
            print(p_page)
            message = f"Subject: {subject}\n\n{message}"
            # server.sendmail(email, person, message)


def main():
    """Do main function."""
    # Get alerts from the past day
    now = datetime.datetime.utcnow()
    day = datetime.timedelta(1)
    yesterday = now - day
    now_str = time_handler.sql_time_str(now)
    yesterday_str = time_handler.sql_time_str(yesterday)
    print(now_str, yesterday_str)
    alerts = bsql.Query(f"SELECT TOP 20 * FROM CEVAC_ALL_ALERTS_HIST_RAW WHERE"
                        f" UTCDateTime BETWEEN '{yesterday_str}' AND "
                        f"'{now_str}' ORDER BY UTCDateTime DESC")
    now_etc = time_handler.utc_to_est(now)
    yesterday_etc = time_handler.utc_to_est(yesterday)
    now_etc_str = time_handler.sql_time_str(now_etc)
    yesterday_etc_str = time_handler.sql_time_str(yesterday_etc)

    alert_dict = alerts.as_dict()
    total_msg = ""
    for i, key in enumerate(alert_dict):
        alert = alert_dict[key]
        id = alert[0].strip()
        type = alert[1].strip()
        message = alert[2].strip()
        metric = alert[3].strip()
        building = alert[4].strip()
        acknowledged = bool(int(alert[6]))
        etc = alert[8].strip()

        e_msg = ""

        if not acknowledged:
            e_msg = (f"{etc}, {metric}, {type}: {message}\n")
            total_msg += e_msg

    subject = f"CEVAC alert log {yesterday_etc_str} - {now_etc_str}"
    email_message(email, password, to_list, total_msg, subject)
