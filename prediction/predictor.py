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
from datetime import date
import numpy as np
# import matplotlib as plt

# fetch our weather forecast
def fetch():
    # json format of the hourly data
    hourly = {
                'hours' : [],
                'days' : [],
                'months' : [],
                'years' : [],
                'humidities' : [],
                'temperatures' : [],
                'clouds' : []
                }

    requestURL = 'https://api.darksky.net/forecast/db6bb38a65d59c7677e8e97db002705b/33.662333,-79.830875'
    r = requests.get(requestURL).json()
    hourlyData = r['hourly']['data']

    # insert every element in the hourly data
    for element in hourlyData:
        hourly['hours'].append(int(time.strftime('%H', time.localtime(element['time']))))
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

    throughMonth = [float(d/numMonth[str(m)])]

    hour = [0 for i in range(0,24)]
    hour[h] = 1

    d = date(y, m, d).weekday()

    day = [0 for i in range(0,7)]
    day[d -1] = 1

    month = [0 for i in range(0,12)]
    month[m - 1] = 1

    return hour, day, month, throughMonth

# prediction with the built-in keras model
def createModel():

	# create the keras instance
	model = keras.Sequential()

	# add layers
	model.add(Dense(100, input_shape=(47,)))
	model.add(Activation('sigmoid'))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(optimizer='adam',loss=losses.mse, metrics=['accuracy'])

	return model

def pred(model):

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
        model.load_weights('powerModel.h5')

        prediction = model.predict(input.reshape(1,-1))[0][0] * 275
        predictions.append(prediction)

    str = ''
    for i, element in enumerate(predictions):

        str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(element, hourly['days'][i], hourly['months'][i], hourly['hours'][i])
    with open('predictions.txt', 'w') as f:
        f.write(str)
    return predictions

if __name__ == '__main__':
    model = createModel()
    predictions = pred(model)
