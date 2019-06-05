## ouput numpy arrays for the keras program to then handles

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import datetime
import time

# read in the data
df = pd.read_csv('WAP_TOTAL_PREDICTED2.csv')


# turns the string of the month into a number
def fixFormat(arg, type):
    if type == 'month':
        months = {
        'JAN' : [1, 'January'],
        'FEB' : [2, 'February'],
        'MAR' : [3, 'March'],
        'APR' : [4, 'April'],
        'MAY' : [5, 'May'],
        'JUN' : [6, 'June'],
        'JUL' : [7, 'July'],
        'AUG' : [8, 'August'],
        'SEP' : [9, 'September'],
        'OCT' : [10, 'October'],
        'NOV' : [11, 'November'],
        'DEC' : [12, 'December']
        }

        return months[arg]

    if type == 'year':
        newYear = '20' + arg
        newYear = int(newYear)
        return newYear

    if type == 'day':
        days = {
        'Monday' : 0,
        'Tuesday' : 1,
        'Wednesday': 2,
        'Thursday' : 3,
        'Friday': 4,
        'Saturday' : 5,
        'Sunday' : 6
        }

        return days[arg]

# formats the date in a way that we can introduce to the array for training
def formatDate():

    # define our information dictionary
    info = {
        'day' : [],
        'month' : [],
         'hour' : [],
         'year' : []
         }

    # seperate the date and omit the year
    for row in df.time:

        # calculate month, day, year, hour
        monthStr = fixFormat(row[2:5], 'month')[1]
        month = fixFormat(row[2:5], 'month')[0]
        day = row[0:2]
        year = fixFormat(row[5:7], 'year')
        hour = int(row[8:10])
        dateString = str(monthStr) + ' ' + str(day) + ', ' + str(year)
        day = datetime.datetime.strptime(dateString, '%B %d, %Y').strftime('%A')
        day = fixFormat(day, 'day')

        # append the calculated information to correct lists
        info['month'].append(month)
        info['year'].append(year)
        info['hour'].append(hour)
        info['day'].append(day)

    # append our new lists to the dataframe
    for key in info:
        df[key] = info[key]
    return df

# create our lists
def theLists():
    tempx = []
    tempy = []
    x = []
    y = []

    for index, row in df.iterrows():
        # temp.append(float(row['assoc_count']))
        tempx.append(float(row['auth_count']))
        tempx.append(float(row['day']))
        tempx.append(float(row['month']))
        tempx.append(float(row['hour']))
        x.append(tempx)
        tempy = [0 for i in range(0,500)]
        tempy[row['occupancy']] = 1
        y.append(tempy)
        tempx = []
    return x, y

# populate our numpy arrays
def makeArrays():

    # call our lists
    x, y = theLists()
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

    return trainingData, trainingLabels, testingData, testingLabels

# make our test arrays to see if kpa is functioning correctly
def testArrays():

    # empty list of the training and testing sets that we are going to make
    trainingData = []
    trainingLabels = []
    # # #
    testingData = []
    testingLabels = []

    x = []
    y = []

    for i in range(0,200):
        tempx = random.randint(0,100)
        tempy = tempx * 2
        tempx = [tempx, tempx * 3]
        x.append(tempx)
        y.append(tempy)
    # this is the dimension of our training dataset
    tDim = int(len(x) * .9)

    for i in range(0, tDim):
        size = len(x)
        num = random.randint(0,size - 1)
        xSelection = x[num]
        ySelection = y[num]
        trainingData.append(xSelection)
        trainingLabels.append(ySelection)
        x.pop(num)
        y.pop(num)

    for i, element in enumerate(x):
        testingData.append(element)
        testingLabels.append(y[i])

    return trainingData, trainingLabels, testingData, testingLabels

if __name__ == '__main__':

    # trainingData, trainingLabels, testingData, testingLabels = testArrays()
    trainingData, trainingLabels, testingData, testingLabels = makeArrays()

    # Saves out numpy arrays so they are not lost in the void
    np.save('trainingData.npy', trainingData)
    np.save('trainingLabels.npy', trainingLabels)
    np.save('testingData.npy', testingData)
    np.save('testingLabels.npy', testingLabels)

    # Debugging nonsense
    print('TESTING DATA:\t\t{} ENTRIES'.format(len(testingData)))
    print('TESTING LABELS:\t\t{} ENTRIES'.format(len(testingLabels)))
    print('TRAINING DATA:\t\t{} ENTRIES'.format(len(trainingData)))
    print('TRAINING LABELS:\t{} ENTRIES'.format(len(trainingLabels)))
