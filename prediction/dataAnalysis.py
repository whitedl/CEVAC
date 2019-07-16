import pandas as pd
import numpy as np

class analyst(object):

    # loads in the database
    def __init__(self, df):
        self.data = pd.read_csv(df, error_bad_lines=False)

    def yieldMax(self, attr):
        print(a.data[attr].max())

    def graph(self, xatt, yatt):
        yield None

    def searchdf(self, attr, val):
        self.attr = attr
        self.val = val
        for name in self.data:
            print(name)
        classes = []
        for index, row in self.data.iterrows():
            # if row['summary'] not in classes:
            #     classes.append(row['summary'])
            if row['summary'] == 'Clear' and int(row['time'][-2:]) > 8 and int(row['time'][-2:]) < 22 and row['apparentTemperature'] > 90:
                print(row)
        # print(classes)
    def showCategories(self):
        for columnName in self.data:
            print(columnName)

    def showClasses(self, column):
        classes = []
        for index, row in self.data.iterrows():
            if row[column] not in classes:
                classes.append(row[column])
        print(classes)

if __name__ == '__main__':
    a = analyst('historicWeather.csv')
    # a.showCategories()
    # a.showClasses('summary')
    # a.yieldMax('temperature')
    a.searchdf(1, 2)
