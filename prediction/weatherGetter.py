import requests
import json
import time
from bs4 import BeautifulSoup
import csv

# list being written to historicWeather.csv
historicWeather = [['time', 'precipIntensity', 'precipProbability', 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'cloudCover', 'uvIndex', 'visibility']]

with open('api.json') as f:
    account = json.load(f)

apiKey = account['key']

def fetch(days):
    try:
        t = str(int(time.time() - 86400 * days))
        url = 'https://api.darksky.net/forecast/' + apiKey + '/33.662333,-79.830875' + ',' + t
        r = requests.get(url).json()
        data = r['hourly']['data']
        appendData(data)
    except:
        print('EXCEPTION')
        pass

def appendData(data):

    # pull relevant data from every hour of the day being queried
    for element in data:
        # create a temporary list to append to the historic data
        temp = []

        for key in ["time", 'precipIntensity', 'precipProbability', 'temperature', 'apparentTemperature', 'humidity', 'cloudCover', 'uvIndex', 'visibility']:
            if key == 'time':
                temp.append(time.strftime('%Y-%B-%d %H', time.localtime(element['time'])))
            else:
                try:
                    temp.append(element[key])
                except:
                    print('NULL ENTRY')
                    temp.append('NULL')

        # add to historic weather
        historicWeather.append(temp)

# write the data in the current dir to the file 'historicWeather.csv'
def writeData():

    with open('historicWeather.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(historicWeather)

if __name__ == '__main__':

    for i in range(40, 0, -1):
        fetch(i)
    writeData()
