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
pdf = pd.read_csv('CEVAC_WATT_POWER_SUMS_HIST_CACHE.csv')
tdf = pd.read_csv('H_WEATHER_TEMP.csv')

# dictionary of dimensions I want to add to the array
dfDict =    {
    'temp' : pd.read_csv('H_WEATHER_TEMP.csv'),
    'clouds' : pd.read_csv('H_WEATHER_CLOUDS.csv'),
    'humidity' : pd.read_csv('H_WEATHER_HUMIDITY.csv')
    }

cJSON = {}

# use this to change the month from a string to num
monat = {
    'JAN' : 1,
    'FEB': 2,
    'MAR' : 3,
    'APR' : 4,
    'MAY' : 5,
    'JUN' : 6,
    'JUL' : 7,
    'AUG' : 8,
    'SEP' : 9,
    'OCT' : 10,
    'NOV' : 11,
    'DEC' : 12
}

# graph some data
def graph():
    array = np.load('accuracy.npy')
    avg = np.mean(array)
    std = np.std(array)
    print(avg, std)

def insertData(df):
    info = {
    'Hour' : [],
    'dayOfWeek' : [],
    'intSum': []
    }

    for index, row in df.iterrows():
        y = int(row['Date'][0:4])
        m = int(row['Date'][5:7])
        d = int(row['Date'][8:10])
        h = int(row['Date'][11:13])
        d = date(y, m, d).weekday()
        intSum = int(row['Sum'])
        info['Hour'].append(h)
        info['dayOfWeek'].append(d)
        info['intSum'].append(intSum)

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
        weatherData = cJSON.get(row['Date'][0:13])
        if weatherData != None:
            temperature = weatherData['temp']
            humidity = weatherData['humidity']
            clouds = weatherData['clouds']
            tempx.append(humidity)
            tempx.append(clouds)
            tempx.append(temperature)
            tempx.append(row['Month'])
            tempx.append(row['Hour'])
            tempx.append(row['dayOfWeek'])
            tempy = [0 for i in range(0,300)]
            tempy[row['intSum']] = 1
            if len(tempx) == 6:
                x.append(tempx)
                y.append(tempy)
            tempx = []

    # empty list of the training and testing sets that we are going to make
    trainingData = []
    trainingLabels = []
    # # #
    testingData = []
    testingLabels = []

    # this is the dimension of our training dataset
    tDim = int(len(x) * .9)

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
    # np.save('powerTrainingData.npy', trainingData)
    # np.save('powerTrainingLabels.npy', trainingLabels)
    # np.save('powerTestingData.npy', testingData)
    # np.save('powerTestingLabels.npy', testingLabels)

    # Debugging nonsense
    # print(trainingData)
    print('TESTING DATA:\t\t{} ENTRIES'.format(len(testingData)))
    print('TESTING LABELS:\t\t{} ENTRIES'.format(len(testingLabels)))
    print('TRAINING DATA:\t\t{} ENTRIES'.format(len(trainingData)))
    print('TRAINING LABELS:\t{} ENTRIES'.format(len(trainingLabels)))

if __name__ =='__main__':
    for key in dfDict:
        formatConditions(dfDict[key], key)
    makeArrays(pdf)
    # graph()
