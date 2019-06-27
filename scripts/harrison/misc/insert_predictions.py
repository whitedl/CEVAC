insert_sql_total = ""

for i, prediction in enumerate(predictions):
        date =  '/'.join((str(hourly['months'][i]), str(hourly['days'][i]), str(hourly['years'][i]))) + ' ' + str(hourly['hours'][i])
        # str = 'INSERT INTO [] ({},{},{})'.format(date, prediction, building, metric)
        insert_sql_total += (f"INSERT INTO table_tODo (date, prediction, building, "
                        f"metric) VALUES ({},{},{},{});")

        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction, hourly['days'][i], hourly['months'][i], hourly['hours'][i])

f = open("/home/bmeares/cache/insert_predictions.sql", "w")
f.write(insert_sql_total.replace(';', '\nGO\n'))
f.close()
os.system("/home/bmeares/scripts/exec_sql_script.sh "
          "/home/bmeares/cache/insert_predictions.sql")
os.remove("/home/bmeares/cache/insert_predictions.sql")
