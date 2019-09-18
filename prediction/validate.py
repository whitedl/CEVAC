import numpy as np
import pandas as pd

# load the data and the labels
data = np.load('powerTrainingData.npy')
labels = np.load('powerTrainingLabels.npy')

# find the nans in numpy array
def findNAN(dataset):
    locations = list(map(tuple, np.where(np.isnan(data))))
    return locations

if __name__ == '__main__':
    print(findNan(data))
