predictions = ""

for i, prediction in enumerate(predictions):
        date =  '/'.join((str(hourly['months'][i]), str(hourly['days'][i]), str(hourly['years'][i]))) + ' ' + str(hourly['hours'][i])
        # str = 'INSERT INTO [] ({},{},{})'.format(date, prediction, building, metric)
        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction, hourly['days'][i], hourly['months'][i], hourly['hours'][i])
