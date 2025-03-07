from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras

from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D
from keras.callbacks import EarlyStopping

# Helper libraries
import os
import numpy as np
from sys import argv
import requests
import json
import time
import datetime
from datetime import date
import numpy as np
import pytz

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

    # fetch the past 12 hours of data starting with 12 hours ago
    for i in range(35, 0, -1):
        requestURL = 'https://api.darksky.net/forecast/db6bb38a65d59c7677e8e97db002705b/33.662333,-79.830875,' + str(int(time.time() - 86400 * i))
        print(requestURL)
        r = requests.get(requestURL).json()
        hourlyData = r['hourly']['data']

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

    # the percent of progress through the month
    throughMonth = [float(d/numMonth[str(m)])]

    # array of hours in the day with a 1 in the hour of the prediciton
    hour = [0 for i in range(0,24)]
    hour[h] = 1

    # array of days of the week with a 1 in the day of the prediction
    d = date(y, m, d).weekday()
    day = [0 for i in range(0,7)]
    day[d -1] = 1

    # array of months of the year with a 1 in the month of the prediction
    month = [0 for i in range(0,12)]
    month[m - 1] = 1

    return hour, day, month, throughMonth

# prediction with the built-in keras model
def createModel():

	# create the keras instance
	model = keras.Sequential()

	# add layers
	model.add(Dense(100, input_shape=(46,)))
	model.add(Activation('sigmoid'))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(optimizer='adam',loss=losses.mse, metrics=['accuracy'])

	return model

# writes the predicitons for the next 48 hours
def pred(model):

    # list of predictions to be populated
    predictions = []
    hourly = fetch()

    # retrieve prediction input for every hour that has data
    for i, hour in enumerate(hourly['hours']):

        day = hourly['days'][i]
        month = hourly['months'][i]
        year = hourly['years'][i]

        # formats and normalizes the data for the numpy array
        hour, day, month, throughMonth = generateInput(hour, day, month, year)
        humidity = [hourly['humidities'][i]]
        temperature = [hourly['temperatures'][i]]
        cloudCoverage = [hourly['clouds'][i]]
        input = np.concatenate((hour, day, month, temperature, humidity, cloudCoverage), axis = -1)
        model.load_weights('powerModel.h5')

        prediction = model.predict(input.reshape(1,-1))[0][0] * 400
        predictions.append(prediction)


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

            t = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
            ETDateTime = t.strftime("%Y-%m-%d %H:%M:%S")

            dst = False
            local = pytz.timezone ("America/New_York")
            naive = datetime.datetime.strptime(datestring, "%a %b %d %H:%M:%S %Y")
            local_dt = local.localize(naive, is_dst=dst)
            t_utc = local_dt.astimezone (pytz.utc)
            UTCDateTime = t_utc.strftime("%Y-%m-%d %H:%M:%S")

            deleteString = ('''DECLARE @utc DATETIME;
            SET @utc = '{}';
            DELETE FROM CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW
            WHERE UTCDateTime = @utc;
            GO
                            ''').format(UTCDateTime)

            insert_sql_total += (deleteString +
                                 "INSERT INTO CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW "
                                 "(UTCDateTime, ETDateTime, Total_Usage) "
                                 f" VALUES('{UTCDateTime}','{ETDateTime}',"
                                 f"'{str(prediction)}')\nGO\n")

    # Write to `CEVAC_WATT_POWER_SUMS_PRED_HIST`
    f = open("/cevac/cache/insert_predictions.sql", "w")
    f.write(insert_sql_total)
    f.close()
    os.system("/cevac/scripts/exec_sql_script.sh "
              "/cevac/cache/insert_predictions.sql")
    os.remove("/cevac/cache/insert_predictions.sql")

if __name__ == '__main__':
    model = createModel()
    pred(model)
