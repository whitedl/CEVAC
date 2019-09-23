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
    a=np.random.randint(0,17849)
    c=np.random.randint(0,17849)
    b=np.random.randint(0,45)
    d=np.random.randint(0,45)

    dataset[a][b]= -1
    dataset[c][d]=1.5
    print("Test 1: a is:",a," and b is:",b)
    print("Test 2: c is:",c," and d is:",d)
    c=0
    counter=0

    for x in np.nditer(dataset):

        if x > 1:
            print("Out of range value is:",x)
            print("<",c,">")
            rowind=int(c/46)
            colind=c%46
            print("Array Index:",rowind, ",",colind)
            counter+=1
        elif x < 0:
            print("Out of range value is:",x)
            print("<",c,">")
            rowind=int(c/46)
            colind=c%46
            print("Array Index:",rowind, ",",colind)
            counter+=1

        c+=1
    if counter==0:
        print("No Values were out of range.")

    print("Done")



if __name__ == '__main__':
    print(findNAN(data))

    verifyData(data)
