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
import csv

class predictor():

    '''
    loads api token data; creates hourly dictionary
    makes empty predictions list to be populated later
    creates model
    makes list of URL endings that are used to get yesterday's, todays, and tomorrows weather
    '''
    def __init__(self):

        # open our api json file and pull the darkSky api key from it
        with open('api.json') as f:
            credentials = json.load(f)

        # api token for [DarkSky][www.darksky.net]
        self.key = credentials['key']

        # dictionary of all of the hourly data from the range(yesterday -> tomorrow)
        self.hourly = {
                    'hours' : [],
                    'days' : [],
                    'months' : [],
                    'years' : [],
                    'humidities' : [],
                    'temperatures' : [],
                    'clouds' : []
                    }

        # input is the array that fetch is going to populate
        self.input = []
        self.predictions = []
        self.model = self.createModel()
        self.urlEndings = ['/33.662333,-79.830875,' + str(int(time.time() - 86400)),
                            '/33.662333,-79.830875,' + str(int(time.time())),
                            '/33.662333,-79.830875']

    # fetch our weather forecast; populates the predictor.hourly dict
    def fetch(self):
        for ending in self.urlEndings:
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

    # returns normalized h, d, m, y, and throughMonth
    def generateInput(self, h, d, m, y):
        numMonth = {
            '1' : 31,
            '2' : 29,
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

    # returns the model with correct dimensions
    def createModel(self):

        # create the keras instance
        model = keras.Sequential()

        # make our initial layer
        model.add(LSTM(256, input_shape=(12, 47), return_sequences=True))
        model.add(Activation('sigmoid'))

        # make our final layer
        model.add(LSTM(units=1))
        model.add(Activation('sigmoid'))

        # specify compiler, loss function, and metrics we want printed out
        model.compile(optimizer='adam',loss=losses.mse, metrics=['accuracy'])

        # load jonathan's brain
        model.load_weights('powerModel.h5')
        # model.load_weights('/home/bmeares/CEVAC/prediction/powerModel.h5')

        return model

    # predict given a power model and the previous 12 hours of weather data
    def predict(self):

        # get information from the past 12 hours
        for i in range(0,12):

            # pull time data from 12 indexes
            hour = self.hourly['hours'][i]
            day = self.hourly['days'][i]
            month = self.hourly['months'][i]
            year = self.hourly['years'][i]

            # formats and normalizes the data for the numpy array
            hour, day, month, throughMonth = self.generateInput(hour, day, month, year)
            humidity = [self.hourly['humidities'][i]]
            temperature = [self.hourly['temperatures'][i]]
            cloudCoverage = [self.hourly['clouds'][i]]
            temp = np.concatenate((hour, day, month, throughMonth, temperature, humidity, cloudCoverage), axis = -1)
            self.input.append(temp)

        self.input = np.array(self.input)

        with open('predInput.txt', 'w') as f:
            f.write(str(self.input))
        prediction = self.model.predict((self.input))

if __name__ == '__main__':

    # make a predictor instance
    predictor = predictor()
    predictor.fetch()
    predictor.predict()
