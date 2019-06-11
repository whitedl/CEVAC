from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras
from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy
import datetime
import os

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
    model.add(Dense(128, input_dim=4))
    model.add(Activation('relu'))
    model.add(Dropout(0.35))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(numClasses))
    model.add(Activation('softmax'))

	# if changes are going to be made to increase accuracy it should be done here
    model.compile(optimizer='rmsprop',loss=losses.categorical_crossentropy, metrics=['accuracy'])
    return model

def train(model):

	# load data
	train_data, train_labels, test_data, test_labels = loadData()

	# stops the model when the loss is no longer decreasing
	# early_stopping = EarlyStopping(monitor='loss', patience=100)

	#more epochs = more work training ~= higher accuracy
	model.fit(train_data, train_labels, epochs=10000, verbose=1) # , callbacks=[early_stopping]

	# for making re-running faster, toggle this to re-run with the same weights from the previous run
	model.save_weights('powerModel.h5')
	# model.load_weights("./checkpoints/weights")	# works in reverse)

	test_loss, test_acc = model.evaluate(test_data, test_labels)

	print('Test accuracy:', test_acc)

def predict(inq):
    # make a model instanace
    model = keras.Sequential([
		keras.layers.Dense(512, input_shape=(3,), activation=tf.nn.relu), #64 was basically a random number for me. I'd experiment with bigger and smaller
		keras.layers.Dropout(0.5),		# makes sure you aren't overfitting and killing your test accuracy. This is a pretty high dropout rate, so make lower as needed (esp if you need a bigger training set)
		keras.layers.Dense(300, activation=tf.nn.relu) #number of neurons in final layer should equal number of classes
	])
    model.compile(optimizer='sgd',loss=losses.categorical_crossentropy, metrics=['accuracy'])
    model.load_weights('powerModel.h5')
    model.predict(inq)

if __name__ == '__main__':
	train(predAlg(300))
    # predict([10, 10, 5])
