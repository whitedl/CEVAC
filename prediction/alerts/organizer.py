import numpy as np
import pandas as pd
import string

pdf=pd.read_csv('sample1.csv')

# print(pdf.shape)
# print(pdf.loc[:,'Metric'])

for i, entry in pdf.iterrows():
    if 'POWER' in entry['Metric']:

        #Trying to sort out data from different metrics to get
        #duration from parameters
        if 'not reported' in entry['AlertMessage']:
            print(entry['AlertID'])
            duration = entry['AlertMessage'][-8:-6];
            print(duration)
