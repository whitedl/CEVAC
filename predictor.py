from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras

from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D
from keras.callbacks import EarlyStopping
from keras.layers.recurrent import LSTM

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

class predictor():

    def __init__(self):
        # open our api json file and pull the darkSky api key from it
        with open('api.json') as f:
            credentials = json.load(f)
        self.key = credentials['key']
        self.hourly = {
                    'hours' : [],
                    'days' : [],
                    'months' : [],
                    'years' : [],
                    'humidities' : [],
                    'temperatures' : [],
                    'clouds' : []
                    }
        self.predictions = []
        self.model = None
        self.urlEndings = ['/33.662333,-79.830875,' + str(time.time() - 86400),
                            '/33.662333,-79.830875,' + str(time.time()),
                            '/33.662333,-79.830875']


    # fetch our weather forecast
    def fetch(self):
        for ending in urlEndings:
            # request url with api key
            requestURL = 'https://api.darksky.net/forecast/' + self.key + ending
            r = requests.get(requestURL).json()
            hourlyData = r['hourly']['data']

            # insert every element in the hourly data
            for element in hourlyData:
                self.hourly['hours'].append(int(time.strftime('%H', time.localtime(element['time']))))
                self.hourly['months'].append(int(time.strftime('%m', time.localtime(element['time']))))
                self.hourly['days'].append(int(time.strftime('%d', time.localtime(element['time']))))
                self.hourly['years'].append(int(time.strftime('%Y', time.localtime(element['time']))))
                self.hourly['humidities'].append(element['humidity'])
                self.hourly['temperatures'].append(((element['temperature'] - 32) / 1.8 + 20) / 70)
                self.hourly['clouds'].append(element['cloudCover'])


    # normalize the hours, days, and months
    def generateInput(self, h, d, m, y):
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
    def createModel(self):

    	# create the keras instance
    	self.model = keras.Sequential()

    	# make our initial layer
    	self.model.add(LSTM(256, input_shape=(12, 47), return_sequences=True))
    	self.model.add(Activation('sigmoid'))

        # make our final layer
    	self.model.add(LSTM(units=1))
    	self.model.add(Activation('sigmoid'))

        # specify compiler, loss function, and metrics we want printed out
    	self.model.compile(optimizer='adam',loss=losses.mse, metrics=['accuracy'])


    def predict(self, model):
        self.model.load_weights('powerModel.h5')
        # model.load_weights('/home/bmeares/CEVAC/prediction/powerModel.h5')

        input = []
        self.hourly = self.fetch()


        for i, hour in enumerate(hourly['hours']):

            day = hourly['days'][i]
            month = hourly['months'][i]
            year = hourly['years'][i]

            # formats and normalizes the data for the numpy array
            hour, day, month, throughMonth = generateInput(hour, day, month, year)
            humidity = [hourly['humidities'][i]]
            temperature = [hourly['temperatures'][i]]
            cloudCoverage = [hourly['clouds'][i]]
            temp = np.concatenate((hour, day, month, throughMonth, temperature, humidity, cloudCoverage), axis = -1)
            input.append(temp)

        prediction = model.predict(input.reshape(1,-1))[0][0] * 275
        self.predictions.append(prediction)

        str = ''

        for i, prediction in enumerate(self.predictions):
            date =  '/'.join((str(hourly['months'][i]), str(hourly['days'][i]), str(hourly['years'][i]))) + ' ' + str(hourly['hours'][i])
            # str = 'INSERT INTO [] ({},{},{})'.format(date, prediction, building, metric)
            str += 'ESTIMATE {} ON {}/{} AT HOUR {}\n'.format(prediction, hourly['days'][i], hourly['months'][i], hourly['hours'][i])

        # write to our predictions text file
        with open('predictions.txt', 'w') as f:
            f.write(str)

if __name__ == '__main__':
    # make a predictor instance
    predictor = predictor()
    predictor.createModel()
    predictor.predict(predictor.model)
