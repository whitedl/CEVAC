import numpy as np
import pandas as pd

'''
Tyler: if you could
1. write a function to check every entry is between 0 and 1
2. write a function to make sure that every trainingData is 46 long 
'''

# load the data and the labels
data = np.load('powerTrainingData.npy')
labels = np.load('powerTrainingLabels.npy')

# find the nans in numpy array
def findNAN(dataset):
    locations = list(map(tuple, np.where(np.isnan(data))))
    return locations

if __name__ == '__main__':
    print(findNAN(data))
