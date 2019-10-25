"""Parse alerts from CEVAC_ALL_ALERTS_HIST."""

import os
import datetime
import smtplib
import ssl
from jinja2 import Template
from email import message as msg
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from time import sleep
import csv
import json
from dateutil import tz

import base64

KNOWN_ISSUES_FPATH = "/cevac/CEVAC/known_issues/Known Data Issues.csv"
email = "cevac5733@gmail.com"
password = "cevacsteve5733"
to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
#    "Bennett Meares": "bmeares@g.clemson.edu",
    #  "Inscribe boi": "bmeares@inscribe.productions",
#    "Zach Smith": "ztsmith@g.clemson.edu",
    # "Zach Klein": "ztklein@g.clemson.edu",
#    "Drewboi": "abemery@clemson.edu",
#    "Tim Howard": "timh@clemson.edu",
}
emergency_to_list = {
    "Harrison Hall": "hchall@g.clemson.edu",
#    "Bennett Meares": "bmeares@g.clemson.edu",
#    "Tim Howard": "timh@clemson.edu",
}

alert_email_html_loc = "/cevac/CEVAC/alerts/alert_system/alert_email.html"
f = open(alert_email_html_loc, "r")
page = Template("".join(f.readlines()))


def encode64(image_fpath):
    """Base64 encode image."""
    return base64.b64encode(open(image_fpath, 'rb').read()).decode('utf-8')


pic_path = "/cevac/CEVAC/alerts/alert_system/pics/"
metrics_a = {
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
    "CO2": {
        "key": "<CO2>",
        "char": "🌫",
    },

    "UNKNOWN": {
        "key": "<UNKNOWN>",
        "char": "📏",
    }
}
metrics_b = {
    "TEMP": {
        "key": "<TEMP>",
        "char": (f"<img src=\"https://i.imgur.com/7idtl34.png\""
                 f" width=\"50\" height=\"50\">"),
    },
    "POWER": {
        "key": "<POWER>",
        "char": (f"<img src=\"https://i.imgur.com/8dxzfpX.png\""
                 f" width=\"50\" height=\"50\">"),
    },
    "IAQ": {
        "key": "<IAQ>",
        "char": (f"<img src=\"https://i.imgur.com/vkFWgSf.png\""
                 f" width=\"50\" height=\"50\">"),
    },
    "CHW": {
        "key": "<CHW>",
        "char": (f"<img src=\"https://i.imgur.com/OtTAHcl.png\""
                 f" width=\"50\" height=\"50\">"),
    },
    "STEAM": {
        "key": "<STEAM>",
        "char": (f"<img src=\"https://i.imgur.com/GdXwxMy.png\""
                 f" width=\"50\" height=\"50\">"),
    },

    "UNKNOWN": {
        "key": "<UNKNOWN>",
        "char": "📏",
    }
}

metrics = {
    "TEMP": {
        "key": "<TEMP>",
        "char": (f"<img src=\"cid:image1\"  width=\"50\" height=\"50\">"),
        "fpath": pic_path + "TEMP.png",
        "cid": "image1",
    },
    "POWER": {
        "key": "<POWER>",
        "char": (f"<img src=\"cid:image2\"  width=\"50\" height=\"50\">"),
        "fpath": pic_path + "POWER.png",
        "cid": "image2",
    },
    "CO2": {
        "key": "<CO2>",
        "char": (f"<img src=\"cid:image3\"  width=\"50\" height=\"50\">"),
        "fpath": pic_path + "CO2.png",
        "cid": "image3",
    },
    "CHW": {
        "key": "<CHW>",
        "char": (f"<img src=\"cid:image4\"  width=\"50\" height=\"50\">"),
        "fpath": pic_path + "CHW.png",
        "cid": "image4",
    },
    "STEAM": {
        "key": "<STEAM>",
        "char": (f"<img src=\"cid:image5\"  width=\"50\" height=\"50\">"),
        "fpath": pic_path + "STEAM.png",
        "cid": "image5",
    },

    "UNKNOWN": {
        "key": "<?>",
        "char": (f"<p>?</p>"),
        "fpath": pic_path + "TEMP.png",
        "cid": "image6",
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
        self.etc = time_of_sql(alert[7])
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


def rebuild_events():
    """Rebuild a broken cache."""
    command = f"EXEC CEVAC_CACHE_INIT @tables = 'CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW'"
    print(command)
    os.system("/cevac/scripts/exec_sql.sh \"" + command +
              "\" temp_csv.csv")
    return None


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
            p_page = page.render(Name=person, message=message, subject=subject,
                                 metrics=metrics)

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
                print(f"<{m['cid']}>")
                msgImage.add_header('Content-ID', f"<{m['cid']}>")
                m_message.attach(msgImage)

            # Define the image's ID as referenced above
            m_message.attach(a_msg)

            new_message = replace_metric(m_message.as_string())
            print(new_message)
            server.sendmail(email, p_email, new_message)


def sql_time_str(t):
    """Return time in sql format."""
    return t.strftime('%Y-%m-%d %H:%M:%S')


def time_of_sql(time_str):
    """Return datetime object of time string."""
    t = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    return t


def est_to_utc(t):
    """Convert est to utc."""
    from_zone = tz.gettz('America/New_York')
    to_zone = tz.gettz('UTC')

    est = t.replace(tzinfo=from_zone)
    utc = est.astimezone(to_zone)
    return utc


def utc_to_est(t):
    """Convert utc to est."""
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    utc = t.replace(tzinfo=from_zone)
    est = utc.astimezone(to_zone)
    return est


class Query:
    """Turn a SELECT query into data."""

    def __init__(self, sql_command):
        """Turn a SELECT sql command into data."""
        if "SELECT" in sql_command.upper():
            self.command = sql_command
            self.json_list = self.request_data(self.command)
        else:
            self.command = None
            self.query = None
            self.json_list = []

    def request_data(self, command):
        """Request data."""
        os.system(f"/cevac/scripts/exec_sql.sh \"{command}\" "
                  "temp1_csv.csv")
        json_string = ""
        headers = {}
        with open("/cevac/cache/temp1_csv.csv", "r") as temp_csv:
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
        data_readable = json_string.replace("\'", "\"")
        data_list = data_readable.split("}{")
        return self._data_list_to_dict_list(data_list)

    def _data_list_to_dict_list(self, data_list):
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

    def as_dict(self, key=None):
        """Return dictionary of data, keyed in as id or key."""
        d = {}
        # Validate key in every dict
        if key is not None:
            for data in self.json_list:
                if key not in data.keys():
                    key = None

        # Make into dict
        if key is None:
            for i, data in enumerate(self.json_list):
                d[i] = data
        else:
            for data in self.json_list:
                d[data[key]] = data

        return d

    def as_json_dict(self):
        """Return dictionary of data, with dicts instead of lists."""
        d = {}
        return d

            
def main():
    """Do main function."""
    # Get alerts from the past day
    rebuild_events()
    try:
        now = datetime.datetime.utcnow()
        day = datetime.timedelta(1)
        yesterday = now - day
        alerts = Query(f" DECLARE @yesterday DATETIME; SET @yesterday = "
                       f"DATEADD(day,"
                       f" -1, GETDATE()); SELECT"
                       f" TOP 100 * FROM CEVAC_ALL_ALERTS_EVENTS_LATEST "
                       f" WHERE ETDateTime >= @yesterday "
                       f" ORDER BY ETDateTime DESC")
        now_etc = utc_to_est(now)
        yesterday_etc = utc_to_est(yesterday)
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
                    e_msg = (f"<td width=\"20%\">{al.etc_str}</td>"
                             f"<td width=\"10%\">{al.metric}</td>"
                             f"<td width=\"70%\">{al.message}</td>")
                    total_msg += e_msg + "</tr>"
                total_msg += "</table>"

        subject = f"CEVAC alert log from {yesterday_etc_str} to {now_etc_str}"
        email_message(email, password, to_list, total_msg, subject)
    except Exception as e:
        print(e)
        f = open("/cevac/DEV/alerts/alert_system/alert_emergency.html",
                 "r")
        emergency_email = "".join(f.readlines())
        email_message(email, password, emergency_to_list,
                      emergency_email, "ISSUES WITH CEVAC ALERTS")

if __name__ == "__main__":
    main()
    

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
