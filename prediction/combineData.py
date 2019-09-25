# import libraries
import json
import random
import numpy as np
import pandas as pd
import string

import datetime as dt
from datetime import date

# historic power readings
pdf = pd.read_csv('CEVAC_WATT_POWER_SUMS_HIST.csv')

# weather dataframe
wdf = pd.read_csv('historicWeather.csv')

# use this to change the month from a string to num
strToNum = {
    'JAN' : '01',
    'FEB': '02',
    'MAR' : '03',
    'APR' : '04',
    'MAY' : '05',
    'JUN' : '06',
    'JUL' : '07',
    'AUG' : '08',
    'SEP' : '09',
    'OCT' : '10',
    'NOV' : '11',
    'DEC' : '12'
}


wdf['powerSum'] = 0


for i, entry in wdf.iterrows():

    weatherDate = entry['time']

    year = weatherDate[0:4]
    month = weatherDate[5:8].upper()
    month = strToNum[month]
    day = weatherDate[-5: -3]
    hour = weatherDate[-2:]
    key = '-'.join((year, month, day))
    key = key + ' ' + hour
    test = []

    nullCounter = 0
    for minute in ['00', '15', '30', '45']:
        key = key + ':' + minute + ':00'
        power = pdf['ETDateTime'] == key
        if len(pdf[power]) != 0:
            power = pdf[power]['Total_Usage'].values[0]
            wdf.set_value(i, 'powerSum', power)

wdf.to_csv('combinedData.csv')
