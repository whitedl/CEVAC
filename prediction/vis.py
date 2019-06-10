# import libraries
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
df = pd.read_csv('CEVAC_WATT_POWER_SUMS_HIST_CACHE.csv')

def insertData():
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

    print(df.describe)

    return df

def makeArrays():
    df = insertData()

    tempx = []
    tempy = []
    x = []
    y = []

    for index, row in df.iterrows():
        tempx.append(row['Month'])
        tempx.append(row['Hour'])
        tempx.append(row['dayOfWeek'])
        tempy = [0 for i in range(0,300)]
        tempy[row['intSum']] = 1
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

    print(trainingData)

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
    makeArrays()
