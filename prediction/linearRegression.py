from sklearn import datasets
from sklearn import metrics
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import scipy
import datetime

df = pd.read_csv('WAP_TOTAL_PREDICTED2.csv')

def fixFormat(arg, type):
    if type == 'month':
        months = {
            'JAN' : [1, 'January'],
            'FEB' : [2, 'February'],
            'MAR' : [3, 'March'],
            'APR' : [4, 'April'],
            'MAY' : [5, 'May'],
            'JUN' : [6, 'June'],
            'JUL' : [7, 'July'],
            'AUG' : [8, 'August'],
            'SEP' : [9, 'September'],
            'OCT' : [10, 'October'],
            'NOV' : [11, 'November'],
            'DEC' : [12, 'December']
        }

        return months[arg]

    if type == 'year':
        newYear = '20' + arg
        newYear = int(newYear)
        return newYear

    if type == 'day':
        days = {
        'Monday' : 0,
        'Tuesday' : 1,
        'Wednesday': 2,
        'Thursday' : 3,
        'Friday': 4,
        'Saturday' : 5,
        'Sunday' : 6
        }

        return days[arg]


def formatDate():

    # define our information dictionary
    info = {
        'day' : [],
        'month' : [],
         'hour' : [],
         'year' : []
         }

    # seperate the date and omit the year
    for row in df.time:
        # calculate month, day, year, hour
        monthStr = fixFormat(row[2:5], 'month')[1]
        month = fixFormat(row[2:5], 'month')[0]
        day = row[0:2]
        year = fixFormat(row[5:7], 'year')
        hour = int(row[8:10])
        dateString = str(monthStr) + ' ' + str(day) + ', ' + str(year)
        day = datetime.datetime.strptime(dateString, '%B %d, %Y').strftime('%A')
        day = fixFormat(day, 'day')

        # append the calculated information to correct lists
        info['month'].append(month)
        info['year'].append(year)
        info['hour'].append(hour)
        info['day'].append(day)

    for key in info:
        df[key] = info[key]

def theLists():
    temp = []
    X = []
    y = []
    for index, row in df.iterrows():
        temp.append(float(row['assoc_count']))
        temp.append(float(row['auth_count']))
        temp.append(row['day'])
        temp.append(float(row['month']))
        temp.append(float(row['hour']))
        X.append(temp)
        y.append(row['occupancy'])
        temp = []
    return X, y

def train():


    formatDate()

    # get our training set
    X, y = theLists()

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
        hidden_layer_sizes=(5, 2), random_state=1)

    clf.fit(X, y)

    MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
                  beta_1=0.9, beta_2=0.999, early_stopping=False,
                  epsilon=1e-08, hidden_layer_sizes=(5, 2),
                  learning_rate='adaptive', learning_rate_init=0.001,
                  max_iter=200, momentum=0.9, n_iter_no_change=10,
                  nesterovs_momentum=True, power_t=0.5, random_state=1,
                  shuffle=True, solver='lbfgs', tol=0.0001,
                  validation_fraction=0.1, verbose=False, warm_start=False)

    # store our results in list
    results = []
    tuples = []

    for index, row in df.iterrows():
        result = clf.predict([[row['assoc_count'], row['auth_count'], row['day'], row['month'], row['hour']]])
        print(row['assoc_count'], row['auth_count'], row['day'], row['month'], row['hour'], result)
        results.append(result)

def linreg():

    formatDate()

    prediction = []
    X, y = theLists()
    model = LinearRegression(n_jobs = -1)
    model.fit(X, y)

    for index, row in df.iterrows():
        prediction.append(model.predict([[row['assoc_count'], row['auth_count'], row['day'], row['month'], row['hour']]])[0])

    slope, intercept, rVal, pVal, stdErr = scipy.stats.linregress(prediction, y)
    rs = rVal**2
    print('R^2 Value:   {}'.format(rs))
    print('STDERR:  {}'.format(stdErr))
    print('N = {}'.format(len(X)))


if __name__ == '__main__':
    train()
    # linreg()
