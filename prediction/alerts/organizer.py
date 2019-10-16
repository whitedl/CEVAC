import numpy as np
import pandas as pd
import string

pdf=pd.read_csv('sample1.csv')

# print(pdf.shape)
# print(pdf.loc[:,'Metric'])

# for i, entry in pdf.iterrows():
#     if 'TEMP' in entry['Metric']:
#
#         #Trying to sort out data from different metrics to get
#         #duration from parameters
#         if 'not reported' in entry['AlertMessage']:
#             # print(entry['AlertID'])
#             duration = entry['AlertMessage'][-8:-6]
#             # print(duration)
#             print(entry['AlertID'],duration);
#
#             if int(duration) > 6:
#                 print('Warning: potentially defective temp sensor')
for i, entry in pdf.iterrows():
    if 'not reported' in entry['AlertMessage']:
        # print(entry['AlertID'])
        warning = ' '
        if 'TEMP' in entry['Metric']:
            duration = entry['AlertMessage'][-8:-6]
            if int(duration)>6:
                warning = 'Warning: temp sensor may be defective'
        else:
            duration = entry['AlertMessage'][-9:-6]
            if 'POWER' in entry['Metric'] and int(duration) > 30:
                warning = 'Warning: Power sensor may be defective'
            elif int(duration)>400:
                warning = 'Warning: CO2 sensor may be defective'
        print(entry['Metric'],entry['AlertID'],duration,warning);
