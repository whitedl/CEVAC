# import libraries
import json
import random
import numpy as np
import pandas as pd
import string

import datetime as dt
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.pylab as plb


# read in the data
pdf = pd.read_csv('CEVAC_WATT_POWER_SUMS_HIST.csv')

# dictionary of dimensions I want to add to the array
''', error_bad_lines=False'''
wdf = pd.read_csv('historicWeather.csv')

#   creates a
cJSON = {}

# use this to change the month from a string to num
monat = {
    'JAN' : '01',
    'FEB': '02',
    'MAR' : '03',
    'APR' : '04',
    'MAY' : '05',
    'JUN' : '06',
    'JUL' : '07',
    'AUG' : '08',
    'SEP' : '09',
    'OCT' : '10',
    'NOV' : '11',
    'DEC' : '12'
}

# return the number of days given a month's number value
numMonth = {
    '01' : 31,
    '02': 29,
    '03' : 31,
    '04' : 30,
    '05' : 31,
    '06' : 30,
    '07' : 31,
    '08' : 31,
    '09' : 30,
    '10' : 31,
    '11' : 30,
    '12' : 31
}


def insertData(df):
    info = {
    'Month' :   [],
    'Hour' : [],
    'dayOfWeek' : [],
    'intSum': [],
    'throughMonth' : []
    }

    for index, row in df.iterrows():

        y = int(row['ETDateTime'][0:4])
        m = int(row['ETDateTime'][5:7])
        d = int(row['ETDateTime'][8:10])
        tm = float(d/numMonth[row['ETDateTime'][5:7]])
        h = int(row['ETDateTime'][-8:-6])

        d = date(y, m, d).weekday()

        intSum = int(row['Total_Usage'])

        info['Month'].append(m)
        info['Hour'].append(h)
        info['dayOfWeek'].append(d)
        info['intSum'].append(intSum)
        info['throughMonth'].append(tm)

    for key in info:
        df[key] = info[key]
    return df

# format our weather data
def formatConditions(df):

    for index, row in df.iterrows():

        # pull the entire date string
        date = row['time']

        # format the year from the date string
        year = str(date[0:4])

        # format the month from the date string
        month = date[5:8]
        month = month.upper()
        month = str(monat[month])

        # format the rest of the time data
        day = str(date[-5:-3])
        hour = str(date[-2:])

        # make the key from the formatted time data
        key = '-'.join((year, month, day))
        key = key + ' ' + hour
        isDict = cJSON.get(key)

        if isDict == None:
            cJSON[key] = {}

        for condition in ['temperature', 'humidity', 'cloudCover', 'uvIndex']:
            cJSON[key][condition] = row[condition]

    with open('combinedData.json', 'w') as f:
        json.dump(cJSON, f)

def makeArrays(df):
    df = insertData(df)

    # temporary x and temporary y lists for each loop
    tempx = []
    tempy = []
    # actual x and y lists of lists
    x = []
    y = []

    # read in our json file
    with open('combinedData.json') as f:
        cJSON = json.load(f)

    dateNotFound = 0

    # populate each array for every row that has all of the attributes
    for index, row in df.iterrows():

        # get our weather data for that date
        try:
            weatherData = cJSON[row['ETDateTime'][0:13]]
        except:
            r = random.randint(0,500)
            if r == 0:
                print(row['ETDateTime'][0:13])
            dateNotFound += 1
            weatherData = None

        if weatherData != None and len(weatherData) == 4:
            # normalize temperature
            temperature = weatherData['temperature']
            temperature = [(temperature + 20) / 70]

            # normalize humidity
            humidity = weatherData['humidity']
            humidity = [(humidity / 100)]

            # one hot encode month
            month = [0 for i in range(0,12)]
            month[row['Month'] - 1] = 1

            # one hot encode hour
            hour = [0 for i in range(0, 24)]
            hour[row['Hour'] - 1] = 1

            # one hot encode day
            day = [0 for i in range(0, 7)]
            day[row['dayOfWeek'] - 1] = 1

            # throughMonth value was already normalized when inserted into df
            throughMonth = [row['throughMonth']]

            # normalize clouds
            clouds = weatherData['cloudCover']
            clouds = [(clouds / 100)]

            tempx = np.concatenate((hour, day, month, throughMonth, temperature, humidity, clouds), axis = -1)
            tempy = [(row['intSum'] / 275)]

            if len(tempx) == 47:
                x.append(tempx)
                y.append(tempy)
            else:
                print(tempx)

    print('DATES NOT FOUND {}'.format(dateNotFound))
    saveArrays(x, y)

def saveArrays(x, y):
    # empty list of the training and testing sets that we are going to make
    trainingData = []
    trainingLabels = []
    # # # # # # # # # # # # #
    testingData = []
    testingLabels = []

    # this is the dimension of our training dataset
    tDim = int(len(x) * .7)

    for i in range(0, tDim):
        size = len(x)
        num = random.randint(0,size - 1)
        xSelection = x[num]
        ySelection = y[num]
        x.pop(num)
        y.pop(num)
        trainingData.append(xSelection)
        trainingLabels.append(ySelection)

    for i, element in enumerate(x):
        testingData.append(element)
        testingLabels.append(y[i])

    # save our numpy arrays
    np.save('powerTrainingData.npy', trainingData)
    np.save('powerTrainingLabels.npy', trainingLabels)
    np.save('powerTestingData.npy', testingData)
    np.save('powerTestingLabels.npy', testingLabels)

    # Debugging nonsense
    print('TESTING DATA:\t\t{} ENTRIES'.format(len(testingData)))
    print('TESTING LABELS:\t\t{} ENTRIES'.format(len(testingLabels)))
    print('TRAINING DATA:\t\t{} ENTRIES'.format(len(trainingData)))
    print('TRAINING LABELS:\t{} ENTRIES'.format(len(trainingLabels)))

if __name__ =='__main__':
    formatConditions(wdf)
    makeArrays(pdf)
