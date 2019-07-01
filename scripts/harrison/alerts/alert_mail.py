"""Parse alerts from CEVAC_ALL_ALERTS_HIST."""

import bsql
import datetime
import time_handler


def main():
    """Do main function."""
    # Get alerts from the past day
    now = datetime.datetime.utcnow()
    day = datetime.timedelta(1)
    yesterday = now - day
    now_str = time_handler.sql_time_str(now)
    yesterday_str = time_handler.sql_time_str(yesterday)
    alerts = bsql.Query(f"SELECT TOP 20 * FROM CEVAC_ALL_ALERTS_HIST WHERE "
                        f"UTCDateTime BETWEEN '{yesterday_str}' AND "
                        f"'{now_str}' ORDER BY UTCDateTime DESC")

    alert_dict = alerts.as_dict()
    for key in alert_dict:
        alert = alert_dict[key]
        id = alert[0].strip()
        type = alert[1].strip()
        message = alert[2].strip()
        metric = alert[3].strip()
        building = alert[4].strip()
        acknowledged = bool(int(alert[5]))
        etc = alert[8].strip()

        if not acknowledged:
            e_msg = (f"{etc}, {metric}, {type}: {message}")
            print(e_msg)
