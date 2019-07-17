# import libraries
import json
import random
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt

# read in the data
# cwdf = pd.read_csv('chwLogs.csv')
pdf = pd.read_csv('CEVAC_WATT_POWER_SUMS_HIST.csv')

weatherDF = pd.read_csv('historicWeather.csv', error_bad_lines=False)

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
        h = int(row['ETDateTime'][11:13])
        d = date(y, m, d).weekday()
        intSum = int(row['Total_Usage'])
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
        key = row['time']
        isDict = cJSON.get(key)
        if isDict == None:
            cJSON[key] = {}
        for condition in ['temperature', 'humidity', 'cloudCover', 'uvIndex']:
            if row[condition] == 'snow' or row[condition] == 'rain':
                pass
            else:
                cJSON[key][condition] = row[condition]
        if len(cJSON[key]) != 4:
            del cJSON[key]

    with open('combinedData.json', 'w') as f:
        json.dump(cJSON, f)

# adds a prescribed number of hours `addition` to the time 'dateTime'
def addHour(dateTime, addition):
    year = str(dateTime[0:4])
    month = str(dateTime[5:7])
    day = str(dateTime[8:10])
    hour = str(dateTime[-2:])

    newYear = None
    newMonth = None
    newDay = None

    newHour = int(hour) + addition

    if newHour > 23:
        newHour = 1
        newDay = int(day) + 1
        day = None

        if newDay > numMonth[month]:
            newMonth = int(month) + 1
            month = None

            if newMonth > 11:
                newMonth = 1
                newYear = int(year) + 1
                year = None

    newDate = []

    for element in [year, newYear, month, newMonth, day, newDay, newHour]:
        if element != None:
            element = str(element)
            if len(element) < 2:
                element = '0' + element
            newDate.append(element)

    newDate = '-'.join((newDate[0], newDate[1], newDate[2])) + ' ' + newDate[3]

    return newDate

# fill numpy arrays for training and testing data sets
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

    # populate each array for every row that has all of the attributes
    for index, row in df.iterrows():

        initialDateTime = row['ETDateTime'][0:13]

        for i in range(0,12):
            newDate = addHour(initialDateTime, i)

            # get our weather data for that date
            try:
                weatherData = cJSON[newDate]
            except:
                weatherData = None

            if weatherData != None and len(weatherData) == 4:
                year = int(newDate[0:4])
                d = int(newDate[8:10])
                m = int(newDate[5:7])
                h = int(newDate[-2:])

                # normalize temperature
                temperature = float(weatherData['temperature'])
                temperature = [((temperature - 32) / 1.8 + 20) / 70]

                # normalize humidity
                humidity = float(weatherData['humidity'])
                humidity = [(humidity / 100)]

                # one hot encode month
                month = [0 for i in range(0,12)]
                month[m - 1] = 1

                # one hot encode hour
                hour = [0 for i in range(0, 24)]
                hour[h - 1] = 1

                # one hot encode day
                day = [0 for i in range(0, 7)]
                d = date(year, m, d).weekday()
                day[d - 1] = 1

                # throughMonth value was already normalized when inserted into df
                throughMonth = [float(d/numMonth[newDate[5:7]])]

                # normalize clouds
                clouds = weatherData['cloudCover']
                clouds = [(clouds / 100)]

                tempx.append(np.concatenate((hour, day, month, throughMonth, temperature, humidity, clouds), axis = -1))

        tempy = [(row['intSum'] / 275)]

        if len(tempx) == 12:
            x.append(tempx)
            y.append(tempy)
        tempx = []

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

    # # save our numpy arrays
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
    formatConditions(weatherDF)
    makeArrays(pdf)
