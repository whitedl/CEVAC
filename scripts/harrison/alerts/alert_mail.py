"""Parse alerts from CEVAC_ALL_ALERTS_HIST."""


import bsql
import datetime
import time_handler
import smtplib
import ssl
from jinja2 import Template
from email import message as msg


email = "cevac5733@gmail.com"
password = "cevacsteve5733"
to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
    # "Bennett Meares": "bmeares@g.clemson.edu",
    # "Inscribe boi": "bmeares@inscribe.productions",
    # "Zach Smith": "ztsmith@g.clemson.edu",
    # "Zach Klein": "ztklein@g.clemson.edu",
    # "Drewboi": "abemery@clemson.edu",
    # "Tim": "timh@clemson.edu",
}
f = open("/cevac/CEVAC/scripts/harrison/alerts/alert_email.html", "r")
page = Template("".join(f.readlines()))

old_metrics = {
    "TEMP": {
        "key": "<TEMP>",
        "char": "🌡",
    },
    "POWER": {
        "key": "<POWER>",
        "char": "⚡",
    },
    "IAQ": {
        "key": "<IAQ>",
        "char": "🌫",
    },
    "CHW": {
        "key": "<CHW>",
        "char": "❄",
    },
    "STEAM": {
        "key": "<STEAM>",
        "char": "⛅",
    },

    "UNKNOWN": {
        "key": "<UNKNOWN>",
        "char": "📏",
    }
}

sz = 5
pic_path = "/cevac/DEV/scripts/harrison/alerts/pics/"
metrics = {
    "TEMP": {
        "key": "<TEMP>",
        "char": (f"<src=\"{pic_path}TEMP.png\" width=\"{sz}em\""
                 f" height=\"{sz}em\">"),
    },
    "POWER": {
        "key": "<POWER>",
        "char": (f"<src=\"{pic_path}POWER.png\" width=\"{sz}em\""
                 f" height=\"{sz}em\">"),
    },
    "IAQ": {
        "key": "<IAQ>",
        "char": (f"<src=\"{pic_path}CO2.png\" width=\"{sz}em\""
                 f" height=\"{sz}em\">"),
    },
    "CHW": {
        "key": "<CHW>",
        "char": (f"<src=\"{pic_path}CHW.png\" width=\"{sz}em\""
                 f" height=\"{sz}em\">"),
    },
    "STEAM": {
        "key": "<STEAM>",
        "char": (f"<src=\"{pic_path}STEAM.png\" width=\"{sz}em\""
                 f" height=\"{sz}em\">"),
    },

    "UNKNOWN": {
        "key": "<UNKNOWN>",
        "char": "📏",
    }
}

class Alert_Log:
    """Handles sorting alerts."""

    def __init__(self, alert):
        """Init."""
        self.type = alert[0].strip()
        self.message = alert[1].strip()
        self.metric = metrics["UNKNOWN"]["key"]
        if alert[2].strip() in metrics:
            self.metric = metrics[alert[2].strip()]["key"]
        self.building = alert[4].strip()
        self.acknowledged = bool(int(alert[5]))
        self.etc = time_handler.time_of_sql(alert[7])
        self.etc_str = self.etc.strftime("%m/%d/%y %I:%M %p")
        return None

    def __lt__(self, other):
        """Return self is less than other."""
        if self.type != other.type:
            return (self.type == "alert")
        if (sorted([self.building, other.building])[1] ==
                self.building and self.building != other.building):
            return False
        if self.etc < other.etc:
            return True
        return True

    def __str__(self):
        """Return string of alert."""
        return f"{self.type}: {self.building}, {self.etc_str}"

    def __repr__(self):
        """Return string of alert."""
        return self.__str__()

    def insert_into_dict(self, dict):
        """Insert into dict."""
        if self.type in dict:
            if self.building in dict[self.type]:
                dict[self.type][self.building].append(self)
            else:
                dict[self.type][self.building] = [self]
        else:
            dict[self.type] = {
                self.building: [self],
            }


def replace_metric(rep_str):
    """Replace metric str with character."""
    for metric in metrics:
        m = metrics[metric]
        rep_str = rep_str.replace(m["key"], m["char"])
    return rep_str


def email_message(email, password, to_list, message, subject):
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
        for person in to_list:
            p_email = to_list[person]
            p_page = page.render(Name=person, message=message, subject=subject)

            m_message = msg.Message()
            m_message.add_header('Content-Type', 'text/html')
            m_message.set_payload(p_page)
            m_message["Subject"] = subject

            new_message = replace_metric(m_message.as_string())
            print(new_message.encode("utf-8"))
            server.sendmail(email, p_email, new_message.encode("utf-8"))


def main():
    """Do main function."""
    # Get alerts from the past day
    now = datetime.datetime.utcnow()
    day = datetime.timedelta(1)
    yesterday = now - day
    alerts = bsql.Query(f" DECLARE @yesterday DATETIME; SET @yesterday = "
                        f"DATEADD(day,"
                        f" -1, GETDATE());"
                        f" SELECT * FROM CEVAC_ALL_ALERTS_EVENTS_HIST "
                        f" WHERE ETDateTime >= @yesterday "
                        f" ORDER BY ETDateTime DESC")
    now_etc = time_handler.utc_to_est(now)
    yesterday_etc = time_handler.utc_to_est(yesterday)
    now_etc_str = now_etc.strftime("%m/%d/%y %I:%M %p")
    yesterday_etc_str = yesterday_etc.strftime("%m/%d/%y %I:%M %p")

    alert_dict = alerts.as_dict()
    total_msg = ""
    all_alerts = []
    for i, key in enumerate(alert_dict):
        alert = alert_dict[key]
        all_alerts.append(Alert_Log(alert))

    all_alerts = sorted(all_alerts)
    alert_gd = {}
    for al in all_alerts:
        al.insert_into_dict(alert_gd)

    total_msg = ""
    for key in alert_gd:
        total_msg += f'<h2 class=\"split\">{key.upper()}</h2>'
        for building in alert_gd[key]:
            total_msg += f"<h4>{building}</h4><table>"
            for al in alert_gd[key][building]:
                total_msg += "<tr>"
                if al.acknowledged:
                    continue
                e_msg = (f"<td>{al.etc_str}</td>"
                         f"<td>{al.metric}</td>"
                         f"<td>{al.message}</td>")
                total_msg += e_msg + "</tr>"
            total_msg += "</table>"

    subject = f"CEVAC alert log from {yesterday_etc_str} to {now_etc_str}"
    email_message(email, password, to_list, total_msg, subject)


'''
    /##.*/
   /#%&&%#/
  ./%%%&%%#
  %%%%&%&%%#
 %&&  %%%&%%.
 %&%  &%%&%%*
 *%&@&@%&%%(
   %%%%%%%%
'''
