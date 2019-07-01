from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras

from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D
from keras.callbacks import EarlyStopping

# Helper libraries
import numpy as np
from numpy import array
from sys import argv
import requests
import json
import time
import datetime
from datetime import date
import numpy as np
import pytz
# import matplotlib as plt

# fetch our weather forecast
def fetch():

    hourly = {
            'hours' : [],
            'weekdayNames' : [],
            'monthNames' : [],
            'seconds' : [],
            'weekNumbers' : [],
            'minutes' : [],
            'months' : [],
            'days' : [],
            'years' : [],
            'humidities' : [],
            'temperatures' : [],
            'clouds' : []
            }

    # request url with api key
    requestURL = 'https://api.darksky.net/forecast/db6bb38a65d59c7677e8e97db002705b/33.662333,-79.830875'
    r = requests.get(requestURL).json()
    hourlyData = r['hourly']['data']
    print(hourlyData[0])

    # insert every element in the hourly data
    for element in hourlyData:
        hourly['hours'].append(int(time.strftime('%H', time.localtime(element['time']))))
        hourly['weekdayNames'].append(str(time.strftime('%a', time.localtime(element['time']))))
        hourly['monthNames'].append(str(time.strftime('%b', time.localtime(element['time']))))
        hourly['seconds'].append(str(time.strftime('%S', time.localtime(element['time']))))
        hourly['weekNumbers'].append(str(time.strftime('%W', time.localtime(element['time']))))
        hourly['minutes'].append(str(time.strftime('%M', time.localtime(element['time']))))
        hourly['months'].append(int(time.strftime('%m', time.localtime(element['time']))))
        hourly['days'].append(int(time.strftime('%d', time.localtime(element['time']))))
        hourly['years'].append(int(time.strftime('%Y', time.localtime(element['time']))))
        hourly['humidities'].append(element['humidity'])
        hourly['temperatures'].append(((element['temperature'] - 32) / 1.8 + 20) / 70)
        hourly['clouds'].append(element['cloudCover'])

<<<<<<< HEAD
    # return json formatted 'hourly' dictionary of lists of hourly data
=======
>>>>>>> origin/prediction
    return hourly

# normalize the hours, days, and months
def generateInput(h, d, m, y):
    numMonth = {
        '1' : 31,
        '2': 29,
        '3' : 31,
        '4' : 30,
        '5' : 31,
        '6' : 30,
        '7' : 31,
        '8' : 31,
        '9' : 30,
        '10' : 31,
        '11' : 30,
        '12' : 31
    }

    # the percent of the month that has elapsed
    throughMonth = [float(d/numMonth[str(m)])]

    # normalized hour of the day for a given data point
    hour = [0 for i in range(0,24)]
    hour[h] = 1

    # returns the day of the week: MONDAY == 0
    d = date(y, m, d).weekday()

    day = [0 for i in range(0,7)]
    day[d -1] = 1

    # normalized month of the year: JANUARY == 0
    month = [0 for i in range(0,12)]
    month[m - 1] = 1

    return hour, day, month, throughMonth

# prediction with the built-in keras model
def createModel():

	# create the keras instance
	model = keras.Sequential()

	# add layers
	model.add(LSTM(256, input_shape=(12, 47), return_sequences=True))
	model.add(Activation('sigmoid'))

	# model.add(LSTM(64, return_sequences=True))
	# model.add(Activation('sigmoid'))

	model.add(LSTM(units=1))
	model.add(Activation('sigmoid'))

	model.compile(optimizer=opt,loss=losses.mse, metrics=['accuracy'])

	return model

def pred(model):
    model.load_weights('powerModel.h5')
    # model.load_weights('/home/bmeares/CEVAC/prediction/powerModel.h5')

    predictions = []
    hourly = fetch()


    for i, hour in enumerate(hourly['hours']):



        day = hourly['days'][i]
        month = hourly['months'][i]
        year = hourly['years'][i]

        # formats and normalizes the data for the numpy array
        hour, day, month, throughMonth = generateInput(hour, day, month, year)
        humidity = [hourly['humidities'][i]]
        temperature = [hourly['temperatures'][i]]
        cloudCoverage = [hourly['clouds'][i]]
        input = np.concatenate((hour, day, month, throughMonth, temperature, humidity, cloudCoverage), axis = -1)

        prediction = model.predict(input.reshape(1,-1))[0][0] * 275
        predictions.append(prediction)

<<<<<<< HEAD
    str = ''

    for i, prediction in enumerate(predictions):
        date =  '/'.join((str(hourly['months'][i]), str(hourly['days'][i]), str(hourly['years'][i]))) + ' ' + str(hourly['hours'][i])
        # str = 'INSERT INTO [] ({},{},{})'.format(date, prediction, building, metric)
        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction, hourly['days'][i], hourly['months'][i], hourly['hours'][i])

    # write to our predictions text file
    with open('predictions.txt', 'w') as f:
        f.write(str)

    return predictions
=======

    insert_sql_total = ''

    for i, prediction in enumerate(predictions):
            m = hourly['months'][i]
            d = (hourly['days'][i] - 1) % 7
            Y = hourly['years'][i]
            H = hourly['hours'][i]

            weekdayName = hourly['weekdayNames'][i]
            day = hourly['days'][i]
            monthName = hourly['monthNames'][i]
            second = hourly['seconds'][i]
            weekNumber = hourly['weekNumbers'][i]
            minute = hourly['minutes'][i]
            month = hourly['months'][i]

            hms = ':'.join((str(H), str(minute), str(second)))
            datestring = ' '.join((weekdayName, monthName, str(day)))

            datestring = datestring + ' ' + hms + ' ' + str(Y)

            # datestring = ' '.join((weekdayName, monthName, str(day), ':'.join((str(H), str(minute), str(second)), str(Y))))

            t = datetime.datetime.strptime(f"{m} {d} {Y} {H}","%m %w %Y %H")

            ETDateTime = t.strftime("%Y-%m-%d %H:%M:%S")

            dst = False
            local = pytz.timezone ("America/New_York")
            naive = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
            local_dt = local.localize(naive, is_dst=dst)
            t_utc = local_dt.astimezone (pytz.utc)
            UTCDateTime = t_utc.strftime("%Y-%m-%d %H:%M:%S")

            insert_sql_total += ("INSERT INTO CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW "
                                 "(UTCDateTime, ETDateTime, Total_Usage) "
                                 f" VALUES({UTCDateTime},{ETDateTime},"
                                 f"{str(prediction)});")

    # Write to `CEVAC_WATT_POWER_SUMS_PRED_HIST`
    f = open("/home/bmeares/cache/insert_predictions.sql", "w")
    f.write(insert_sql_total.replace(';', '\nGO\n'))
    f.close()
    os.system("/CEVAC/scripts/exec_sql_script.sh "
              "/CEVAC/cache/insert_predictions.sql")
    os.remove("/CEVAC/cache/insert_predictions.sql")

>>>>>>> origin/prediction

if __name__ == '__main__':
    model = createModel()
    predictions = pred(model)
