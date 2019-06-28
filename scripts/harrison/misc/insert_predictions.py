import pytz
import datetime

insert_sql_total = ""

for i, prediction in enumerate(predictions):
        m = hourly['months'][i]
        d = (hourly['days'][i] - 1) % 7
        Y = hourly['years'][i]
        H = hourly['hours'][i]
        t = datetime.datetime.strptime(f"{m} {d} {Y} {H}","%m %w %Y %H")
        ETDateTime = t.strftime("%Y-%m-%d %H:%M:%S")

        dst = False
        local = pytz.timezone ("America/New_York")
        naive = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
        local_dt = local.localize(naive, is_dst=dst)
        t_utc = local_dt.astimezone (pytz.utc)
        UTCDateTime = t_utc.strftime("%Y-%m-%d %H:%M:%S")

        insert_sql_total += ("INSERT INTO CEVAC_WATT_POWER_SUMS_PRED_HIST "
                             "(UTCDateTime, ETDateTime, PredictedUsage) "
                             f"metric) VALUES({UTCDateTime},{ETDateTime},"
                             f"{str(prediction)});")

        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction,
                                                          hourly['days'][i],
                                                          hourly['months'][i],
                                                          hourly['hours'][i])

# Write to `CEVAC_WATT_POWER_SUMS_PRED_HIST`
f = open("/home/bmeares/cache/insert_predictions.sql", "w")
f.write(insert_sql_total.replace(';', '\nGO\n'))
f.close()
os.system("/home/bmeares/scripts/exec_sql_script.sh "
          "/home/bmeares/cache/insert_predictions.sql")
os.remove("/home/bmeares/cache/insert_predictions.sql")
