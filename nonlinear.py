import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import datetime
import time

# read in the data
df = pd.read_csv('WAP_TOTAL_PREDICTED2.csv')

def disp():
    plt.scatter(df.day, df.auth_count, color='C1')
    plt.scatter(df.day, df.occupancy, color='C3')

def format():
    # list of which hour of the week the entry took place
    hours = []

    #
    for index, row in df.iterrows():
        day = row['day']
        hour = row['hour']
        hourOfWeek = int(hour) + (day - 1) * 24
        hours.append(hourOfWeek)
    df['hourOfWeek'] = hours

def visualise():
    # the day of the week (1-7), each individual week's data,
    # and lastly the list of every week's list of data
    day = None
    week = []
    weeks = []
    occupancy = []

    for index, row in df.itterrows():
        if day == 7 and row['day'] == 1:
            weeks.append([week, occupancy])
            week = []
            occupancy = []
        week.append(row['day'])
        occupancy.append(row['occupancy'])
if __name__ == '__main__':
    visualise()
