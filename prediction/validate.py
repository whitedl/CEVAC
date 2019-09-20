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

def verifyData(dataset):
    rangecount=0
    c=0
    vdata=dataset.tolist()
    print(type(dataset))
    # print(len(vdata))
    #print(vdata)
    # for rindex,row in vdata:
    #
    #      print(len(row))
    #         print(vdata[rindex][0])
    #     if c >= 1.00:
    #         print("Value ", index, "is greater than 1")
    #         rangecount+=1
    #     elif c <= 0.00:
    #         print("Value ", index, "is less than 0")
    #         rangecount+=1
    # if rangecount==0:
    #     print("All values are within range")
    # return None

##in enumerate(vdata):

if __name__ == '__main__':
    print(findNAN(data))

    verifyData(data)
    print("test\n")
