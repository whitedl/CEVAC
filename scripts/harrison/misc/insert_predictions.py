insert_sql_total = ""

for i, prediction in enumerate(predictions):
        # date needs to be string in format '%Y-%m-%d %H:%M:%S' eg "2019-06-26 11:30:39.000"
        # I can't run it on the server for whatever reason, so I don't know the format of the date below,
        # or the hourly variable
        date =  '/'.join((str(hourly['months'][i]), str(hourly['days'][i]), str(hourly['years'][i]))) + ' ' + str(hourly['hours'][i])

        # Bennett hasn't told me table name or column names, so those need to change
        # in the first set of parenthesese
        insert_sql_total += (f"INSERT INTO table_tODo (date, prediction, building, "
                        f"metric) VALUES({},{str(prediction)},{building},{metric});")

        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction, hourly['days'][i], hourly['months'][i], hourly['hours'][i])

f = open("/home/bmeares/cache/insert_predictions.sql", "w")
f.write(insert_sql_total.replace(';', '\nGO\n'))
f.close()
os.system("/home/bmeares/scripts/exec_sql_script.sh "
          "/home/bmeares/cache/insert_predictions.sql")
os.remove("/home/bmeares/cache/insert_predictions.sql")
