# import libraries
import json
import random
import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.pylab as plb


# read in the data
cwdf = pd.read_csv('chwLogs.csv')
temp = pd.read_csv('TMY3_StationsMeta.csv')

# dictionary of dimensions I want to add to the array
dfDict =    {
    'temp' : pd.read_csv('H_WEATHER_TEMP.csv'),
    'clouds' : pd.read_csv('H_WEATHER_CLOUDS.csv'),
    'humidity' : pd.read_csv('H_WEATHER_HUMIDITY.csv')
    }

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
def formatConditions(df, condition):
    for index, row in df.iterrows():
        date = row['time'][0:12]
        year = str(date[5:9])
        month = str(monat[date[2:5]])
        day = str(date[0:2])
        hour = str(date[10:12])
        key = '-'.join((year, month, day))
        key = key + ' ' + hour
        isDict = cJSON.get(key)
        if isDict == None:
            cJSON[key] = {}
        cJSON[key][condition] = row['value']

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

    # populate each array for every row that has all of the attributes
    for index, row in df.iterrows():

        # get our weather data for that date
        try:
            weatherData = cJSON[row['ETDateTime'][0:13]]
        except:
            weatherData = None

        if weatherData != None and len(weatherData) == 3:
            # normalize temperature
            temperature = weatherData['temp']
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
            clouds = weatherData['clouds']
            clouds = [(clouds / 100)]

            tempx = np.concatenate((hour, day, month, throughMonth, temperature, humidity, clouds), axis = -1)
            tempy = [(row['intSum'] / 275)]

            if len(tempx) == 47:
                x.append(tempx)
                y.append(tempy)

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
    for key in dfDict:
        formatConditions(dfDict[key], key)
    makeArrays(pdf)
