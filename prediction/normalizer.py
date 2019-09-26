# import libraries
import json
import random
import numpy as np
import pandas as pd
import string

import datetime as dt
from datetime import date

# read in the csv
df = pd.read_csv('combinedData.csv')

strToNum = {
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

def makeArrays(df):
    # temporary x and temporary y lists for each loop
    tempx = []
    tempy = []

    # actual x and y lists of lists
    x = []
    y = []

    dateNotFound = 0

    # populate each array for every row that has all of the attributes
    for index, row in df.iterrows():

        # load the time / weather data from that row
        weatherData = df.iloc[index]

        # format the time data
        time = weatherData['time']
        monthValue = strToNum[time[5:8].upper()]
        year = int(time[:4])
        dayValue = int(time[-5:-3])
        dayOfWeek =  date(year, monthValue, dayValue).weekday()
        hourValue = int(time[-2:])


        # normalize temperature
        temperature = weatherData['temperature']
        temperature = [(temperature + 20) / 150]
        if temperature[0] > 1:
            print('Temperature:\t{}'.format(temperature[0]))

        # normalize humidity
        humidity = weatherData['humidity']
        humidity = [(humidity / 100)]

        # one hot encode month
        month = [0 for i in range(0,12)]
        month[monthValue - 1] = 1

        # one hot encode hour
        hour = [0 for i in range(0, 24)]
        hour[hourValue - 1] = 1

        # one hot encode day
        day = [0 for i in range(0, 7)]
        day[dayOfWeek - 1] = 1

        # throughMonth value was already normalized when inserted into df
        # throughMonth = [row['throughMonth']]

        # normalize clouds
        clouds = weatherData['cloudCover']
        clouds = [(clouds / 100)]

        # concatenate all of the lists
        tempx = np.concatenate((hour, day, month, temperature, humidity, clouds), axis = -1)

        if not np.isnan(tempx).any():
            powerSum = weatherData['powerSum']
            # if powerSum < 0.1 or powerSum > .9:
            #     print('Power Sum:\t{}'.format(powerSum))
            tempy = 

            # if powerSum > 0.01:
            x.append(tempx)
            y.append(tempy)
        else:
            print('OMITTED')
    return x, y

def saveArrays(x, y):
    # empty list of the training and testing sets that we are going to make
    trainingData = []
    trainingLabels = []
    # # # # # # # # # # # # #
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
    np.save('powerTrainingData.npy', trainingData)
    np.save('powerTrainingLabels.npy', trainingLabels)
    np.save('powerTestingData.npy', testingData)
    np.save('powerTestingLabels.npy', testingLabels)

    # Debugging nonsense
    print('TESTING DATA:\t\t{} ENTRIES'.format(len(testingData)))
    print('TESTING LABELS:\t\t{} ENTRIES'.format(len(testingLabels)))
    print('TRAINING DATA:\t\t{} ENTRIES'.format(len(trainingData)))
    print('TRAINING LABELS:\t{} ENTRIES'.format(len(trainingLabels)))

if __name__ == '__main__':
    x, y = makeArrays(df)
    saveArrays(x, y)
