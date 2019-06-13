from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras
# from tensorflow.keras.callbacks import EarlyStopping
from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D

# Helper libraries
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy
import datetime
import os
import random

# read in our data
def loadData():

	train_data = np.load("powerTrainingData.npy")
	train_labels = np.load("powerTrainingLabels.npy")

	test_data = np.load("powerTestingData.npy")
	test_labels = np.load("powerTestingLabels.npy")

	train_data = train_data / train_data.max()
	test_data = test_data / test_data.max()

	return train_data, train_labels, test_data, test_labels

# prediction with the built-in keras model
def predAlg(numClasses):
	# the capacity of the building
    class_names = [i for i in range(0,numClasses)]	#these are your possible outputs (number of devices on the wifi

	# create the keras instance
    model = keras.Sequential()
    model.add(Dense(512, input_shape=(6,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.35))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(300))
    model.add(Activation('softmax'))

	# if changes are going to be made to increase accuracy it should be done here
    model.compile(optimizer='adam',loss=losses.categorical_crossentropy, metrics=['accuracy'])

    return model

# trains the model
def train(model):

    # load data
    train_data, train_labels, test_data, test_labels = loadData()

    # stops the model when the loss is no longer decreasing
    # early_stopping = EarlyStopping(monitor='loss', patience=15)

    #more epochs = more work training ~= higher accuracy
    model.fit(train_data, train_labels, epochs=1250, verbose=1) # , callbacks=[early_stopping]

    # for making re-running faster, toggle this to re-run with the same weights from the previous run
    model.save_weights('powerModel.h5')
    # model.load_weights("./checkpoints/weights")	# works in reverse)

    test_loss, test_acc = model.evaluate(test_data, test_labels)

    print('Test accuracy:', test_acc)

# loads weights and makes a prediction
def predict(inq):
    # make a model instanace
    model = keras.Sequential()
    model.add(Dense(512, input_shape=(6,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.35))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    # model.add(Dense(256))
    # model.add(Activation('relu'))
    # model.add(Dense(64))
    # model.add(Activation('relu'))
    # model.add(Dense(512))
    # model.add(Activation('relu'))
    model.add(Dense(300))
    model.add(Activation('softmax'))

	# if changes are going to be made to increase accuracy it should be done here
    # model.compile(optimizer='adam',loss=losses.categorical_crossentropy, metrics=['accuracy'])
    model.load_weights('powerModel.h5')
    x = model.predict(inq)
    choice = 0
    num = -1
    for i, ran in enumerate(x[0]):
        if ran > choice:
            choice = ran
            num = i
    return num

# calculates and displays accuracy
def disp():
    results = []
    testingData = np.load('powerTestingData.npy')
    testingLabels = np.load('powerTestingLabels.npy')
    for index, element in enumerate(testingData):
        y = testingLabels[index]
        for ind, el in enumerate(y):
            if el == 1:
                yIndex = ind
        y = yIndex
        prediction = predict(element.reshape(1,-1))
        err = (((prediction - y) / y)**2)**.5 * 100
        results.append(err)
        print('ERROR:\t{}\t\tPREDICTION:\t{}'.format(int(err), prediction))
    return(results)

if __name__ == '__main__':
	train(predAlg(300))
    # disp()

# [[ 78.     1.     6.03  12.    21.     2.  ]
#  [ 50.     1.    12.49  11.    19.     2.  ]
#  [100.    90.     8.04  12.    18.     4.  ]
#  ...
#  [ 72.    75.    23.    11.    15.     3.  ]
#  [ 47.     1.    14.    11.    13.     4.  ]
