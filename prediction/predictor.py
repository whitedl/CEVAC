from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras

from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D
from keras.callbacks import EarlyStopping

# Helper libraries
import numpy as np
from numpy import array
from sys import argv


def generateInput(h, d, m):
    hour = [0 for i in range(0,24)]
    hour[h] = 1

    day = [0 for i in range(0,7)]
    day[d] = 1

    month = [0 for i in range(0,12)]
    month[m] = 1

    return hour, day, month

# prediction with the built-in keras model
def createModel():

	# create the keras instance
	model = keras.Sequential()

	# add layers
	model.add(Dense(128, input_shape=(46,)))
	model.add(Activation('sigmoid'))
	#
	# model.add(Dense(64))
	# model.add(Activation('sigmoid'))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(optimizer='adam',loss=losses.mse, metrics=['accuracy'])

	return model

def pred(model, input):

    model.load_weights('powerModel.h5')

    prediction = model.predict(input) * 275

    return prediction

if __name__ == '__main__':
    h = int(argv[1])
    d = int(argv[2])
    m = int(argv[3])
    temperature = [(float(argv[4]) + 20) / 70]
    humidity = [float(argv[5])]
    clouds = [float(argv[6])]
    hour, day, month = generateInput(h, d, m)
    # temperature, humidity, clouds = getWeather()
    inputArray = np.concatenate((hour, day, month, temperature, humidity, clouds), axis = -1)
    model = createModel()
    prediction = pred(model, inputArray.reshape(1,-1))
    print(prediction[0][0])
