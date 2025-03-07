"""Parse alerts from CEVAC_ALL_ALERTS_HIST."""

import os
import datetime
from dateutil import tz
import smtplib
import ssl
from jinja2 import Template
from email import message as msg
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pandas as pd
import pyodbc
import base64
import sys

FILE_FPATH = "/cevac/cron/email/page/issues.html"
email = "cevac5733@gmail.com"
password = "cevacsteve5733"
to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
    "Bennett Meares": "bmeares@g.clemson.edu",
    #  "Inscribe boi": "bmeares@inscribe.productions",
    "Zach Smith": "ztsmith@g.clemson.edu",
    # "Zach Klein": "ztklein@g.clemson.edu",
    "Drewboi": "abemery@g.clemson.edu",
    "Tyler Piel": "tpiel@g.clemson.edu",
    "Tim Howard": "timh@clemson.edu",
    #  "Dhruv Jain": "djain@clemson.edu",
    "FILE": FILE_FPATH,
}
emergency_to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
    "Bennett Meares": "bmeares@g.clemson.edu",
    "Tim Howard": "timh@clemson.edu",
}
debug_to_list = {
    "DEBUG Hall": "hchall@g.clemson.edu"
}

f = open("emails/html/alert_email.html", "r")
page = Template("".join(f.readlines()))


def encode64(image_fpath):
    """Base64 encode image."""
    return base64.b64encode(
        open(
            image_fpath, 'rb'
        ).read()
    ).decode('utf-8')


pic_path = "emails/pics/"
hard_html_pic_path = "/cevac_alerts/pics/"
metrics = {
    "TEMP": {
        "key": "<TEMP>",
        "char": (f"<img src=\"cid:image1\" "
                 " width=\"50\" height=\"50\">"),
        "fpath": pic_path + "TEMP.png",
        "cid": "image1",
        "htmlpath": hard_html_pic_path + "TEMP.png",
    },
    "POWER": {
        "key": "<POWER>",
        "char": (f"<img src=\"cid:image2\"  "
                 "width=\"50\" height=\"50\">"),
        "fpath": pic_path + "POWER.png",
        "cid": "image2",
        "htmlpath": hard_html_pic_path + "POWER.png",
    },
    "CO2": {
        "key": "<CO2>",
        "char": (f"<img src=\"cid:image3\" "
                 "width=\"50\" height=\"50\">"),
        "fpath": pic_path + "CO2.png",
        "cid": "image3",
        "htmlpath": hard_html_pic_path + "CO2.png",
    },
    "CHW": {
        "key": "<CHW>",
        "char": (f"<img src=\"cid:image4\"  "
                 "width=\"50\" height=\"50\">"),
        "fpath": pic_path + "CHW.png",
        "cid": "image4",
        "htmlpath": hard_html_pic_path + "CHW.png",
    },
    "STEAM": {
        "key": "<STEAM>",
        "char": (f"<img src=\"cid:image5\"  "
                 "width=\"50\" height=\"50\">"),
        "fpath": pic_path + "STEAM.png",
        "cid": "image5",
        "htmlpath": hard_html_pic_path + "STEAM.png",
    },
    "HUM": {
        "key": "<HUM>",
        "char": (f"<p>%</p>"),
        "fpath": pic_path + "TEMP.png",
        "cid": "image6",
        "htmlpath": hard_html_pic_path + "TEMP.png",
    },

    "UNKNOWN": {
        "key": "<?>",
        "char": (f"<p>?</p>"),
        "fpath": pic_path + "TEMP.png",
        "cid": "image6",
        "htmlpath": hard_html_pic_path + "TEMP.png",
    }
}

priority = {
    "-1": "CEVAC",
    -1 : "CEVAC",
    "0": "N/A",
    0 : "N/A",
    "1": "Low",
    1 : "Low",
    "2": "High",
    2 : "High",
}


class Email:
    """OO manage email."""

    def __init__(self, hours=24, verbose=False, conn=None, logging=None):
        """Object oriented version for emails."""
        self.hours = hours
        self.verbose = verbose
        self.conn = conn
        if conn is None:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=130.127.218.11;DATABASE=WFIC-CEVAC;'
                'UID=wficcm;PWD=5wattcevacmaint$'
            )
        if logging is None:
            self.LOG = False
            self.logging = None
        else:
            self.LOG = True
            self.logging = logging

    def write_to_file(self):
        """Write email to file."""
        query = (
            "DECLARE @yesterday DATETIME; "
            "SET @yesterday = DATEADD("
            "day, -1, GETDATE()); "
            "SELECT * FROM "
            "CEVAC_ALL_ALERTS_EVENTS_HIST_RAW "
            "WHERE latest_UTC >= @yesterday "
            "ORDER BY latest_UTC DESC"
        )
        alerts = pd.read_sql_query(
            query,
            self.conn
        )
        now_etc = self.utc_to_est(datetime.datetime.utcnow())
        yesterday_etc = self.utc_to_est(
            datetime.datetime.utcnow()-datetime.timedelta(1)
        )
        now_etc_str = now_etc.strftime(
            "%m/%d/%y %I:%M %p"
        )
        yesterday_etc_str = yesterday_etc.strftime(
            "%m/%d/%y %I:%M %p"
        )

        total_msg = ""
        all_alerts = []
        for i in range(len(alerts)):
            all_alerts.append(Alert_Log(alerts, i))
            
        all_alerts = sorted(all_alerts)
        alert_gd = {}
        for al in all_alerts:
            al.insert_into_dict(alert_gd)

        total_msg = ""
        for key in alert_gd:
            p = str(priority.get(key, key))
            total_msg += f'<h2 class=\"split\">{p}</h2>'
            for building in alert_gd[key]:
                total_msg += f"<h4>{building}</h4><table>"
                for al in alert_gd[key][building]:
                    total_msg += "<tr>"
                    if al.acknowledged:
                        continue
                    e_msg = (f"<td width=\"20%\">{al.etc_str}</td>"
                             f"<td width=\"10%\">{al.metric}</td>"
                             f"<td width=\"70%\">{al.message}</td>")
                    total_msg += e_msg + "</tr>"
                total_msg += "</table>"

        subject = (f"CEVAC alert log from {yesterday_etc_str} to "
                   f"{now_etc_str}")
        p_page = page.render(
            Name="CEVAC", message=total_msg,
            subject=subject, metrics=metrics
        )
        
        m_message = MIMEMultipart()

        a_msg = msg.Message()
        a_msg.add_header('Content-Type', 'text/html')
        a_msg.set_payload(p_page)
        m_message["Subject"] = subject

        for i, metric in enumerate(metrics):
            m = metrics[metric]

        # Define the image's ID as referenced above
        m_message.attach(a_msg)
            
        new_message = self.replace_metric(
            m_message.as_string(),
            html=True
        )
        
        if self.verbose:
            print(new_message)
            
        f_name = to_list["FILE"]
        html_file = open(f_name, "w")
        real_html = new_message[new_message.find("<html>"):]
        real_html = real_html[:(
            real_html.find("<h2 class=\"split\">Symbol")
            -1
        )]
        real_html += "</div></body></html>"
        html_file.write(real_html)

    def send(self, debug=False):
        """Do main function."""
        # Get alerts from the past day
        # self.rebuild_events() TODO?
        query = (
            "DECLARE @yesterday DATETIME; "
            "SET @yesterday = DATEADD("
            "day, -1, GETDATE()); "
            "SELECT * FROM "
            "CEVAC_ALL_ALERTS_EVENTS_HIST_RAW "
            "WHERE latest_UTC >= @yesterday "
            "ORDER BY latest_UTC DESC"
        )
        alerts = pd.read_sql_query(
            query,
            self.conn
        )
        now_etc = self.utc_to_est(datetime.datetime.utcnow())
        yesterday_etc = self.utc_to_est(
            datetime.datetime.utcnow()-datetime.timedelta(1)
        )
        now_etc_str = now_etc.strftime(
            "%m/%d/%y %I:%M %p"
        )
        yesterday_etc_str = yesterday_etc.strftime(
            "%m/%d/%y %I:%M %p"
        )

        total_msg = ""
        all_alerts = []
        for i in range(len(alerts)):
            all_alerts.append(Alert_Log(alerts, i))
            
        all_alerts = sorted(all_alerts)
        alert_gd = {}
        for al in all_alerts:
            al.insert_into_dict(alert_gd)

        total_msg = ""
        for key in alert_gd:
            if key == 0:
                continue
            p = str(priority.get(key, key))
            total_msg += f'<h2 class=\"split\">{p}</h2>'
            for building in alert_gd[key]:
                total_msg += f"<h4>{building}</h4><table>"
                for al in alert_gd[key][building]:
                    total_msg += "<tr>"
                    if al.acknowledged:
                        continue
                    e_msg = (f"<td width=\"20%\">{al.etc_str}</td>"
                             f"<td width=\"10%\">{al.metric}</td>"
                             f"<td width=\"70%\">{al.message}</td>")
                    total_msg += e_msg + "</tr>"
                total_msg += "</table>"

        subject = (f"CEVAC alert log from {yesterday_etc_str} to "
                   f"{now_etc_str}")
        if not debug:
            self.email_message(
                email, password, to_list,
                total_msg, subject
            )
        else:
            self.email_message(
                email, password, debug_to_list,
                total_msg, subject
            )
        

    def rebuild_events(self):
        """Rebuild a broken cache."""
        cursor = self.conn.cursor()
        command = (f"EXEC CEVAC_CACHE_INIT @tables = "
                   "'CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW'")
        cursor.execute(command)
        cursor.commit()
        self.conn.commit()
        cursor.close()
        if self.verbose:
            print(command)
        return None

    def email_message(self, email, password, to_list, message, subject):
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
                p_page = page.render(
                    Name=person, message=message,
                    subject=subject, metrics=metrics
                )

                m_message = MIMEMultipart()

                a_msg = msg.Message()
                a_msg.add_header('Content-Type', 'text/html')
                a_msg.set_payload(p_page)
                m_message["Subject"] = subject

                for i, metric in enumerate(metrics):
                    m = metrics[metric]
                    fp = open(m["fpath"], 'rb')
                    msgImage = MIMEImage(fp.read())
                    fp.close()
                    if self.verbose:
                        print(f"<{m['cid']}>")
                    msgImage.add_header('Content-ID', f"<{m['cid']}>")
                    m_message.attach(msgImage)

                # Define the image's ID as referenced above
                m_message.attach(a_msg)

                new_message = self.replace_metric(m_message.as_string())
                if self.verbose:
                    print(new_message)
                if person == "FILE":
                    pass
                    #html_file = open(p_email, "w")
                    #html_file.write(new_message)
                else:
                    server.sendmail(email, p_email, new_message)

    def replace_metric(self, rep_str, html=False):
        """Replace metric str with character."""
        if not html:
            for metric in metrics:
                m = metrics[metric]
                rep_str = rep_str.replace(m["key"], m["char"])
            return rep_str
        else:
            for metric in metrics:
                m = metrics[metric]
                rep_str = rep_str.replace(
                    m["key"],
                    f"<img width=\"50%\" src=\"{m['htmlpath']}\">",
                )
            return rep_str

    def utc_to_est(self, t):
        """Convert utc to est."""
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')

        utc = t.replace(tzinfo=from_zone)
        est = utc.astimezone(to_zone)
        return est


class Alert_Log:
    """Handles sorting alerts."""

    def __init__(self, alerts, i):
        """Init."""
        self.type = alerts["AlertType"][i]
        self.message = alerts["AlertMessage"][i].strip()
        self.metric = metrics["UNKNOWN"]["key"]
        if alerts["Metric"][i].strip() in metrics:
            self.metric = metrics[alerts["Metric"][i].strip()]["key"]
        self.building = alerts["BuildingSName"][i].strip()
        self.acknowledged = alerts["Acknowledged"][i]
        self.etc = alerts["latest_UTC"][i]  
        self.etc_str = self.etc.strftime("%m/%d/%y %I:%M %p")
        return None

    def __lt__(self, other):
        """Return self is less than other."""
        if self.type != other.type:
            return (self.type == "alert")
        if (sorted([self.building, other.building])[1] ==
                self.building and self.building != other.building):
            return False
        if self.metric != other.metric:
            if self.metric < other.metric:
                return True
            else:
                return False
        if (self.get_room_number() != other.get_room_number()):
            if (self.get_room_number() < other.get_room_number()):
                return True
            else:
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

    def get_room_number(self):
        """Get room number from phrase."""
        phrase = self.message.split(" ")[0]
        if not self.contains_number(phrase):
            return ""
        return phrase

    def contains_number(self, phrase):
        """Return True if string contains number."""
        for i in phrase:
            if str.isdigit(i):
                return True
        return False

    def time_of_sql(time_str):
        """Return datetime object of time string."""
        t = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
        return t


if __name__ == "__main__":
    import os
    print(os.listdir())
    todo = input("email [a]ll, [d]ebug email, [u]pdate webpage: ").lower()
    email_setup = Email(verbose=True)
    if 'a' in todo:
        email_setup.send()
    if 'd' in todo:
        email_setup.send(debug=True)
    if 'u' in todo:
        email_setup.write_to_file()



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
