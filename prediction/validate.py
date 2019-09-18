import numpy as np
import pandas as pd

# load the data and the labels
data = np.load('powerTrainingData.npy')
labels = np.load('powerTrainingLabels.npy')

for d in data:
    print(d)
    for entry in d:
        if entry > 1:
            print(entry)
