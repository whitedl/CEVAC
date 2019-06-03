'''
General note for your data - I'd ranndomly chunk it up so 90% is training data, and ~10% is test. The lowest you probably
wanna go for test data is 5% of your original set. If you need more data, I'd just make up/generate some realistic cases.
'''

from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from keras import losses
from keras.utils import plot_model

# local libs
import dataSplitter

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy
import datetime
import os

def vis():
	# get out x and y values
	x, y = dataSplitter.theLists()

	df = dataSplitter.formatDate()

	# make our correlation plot
	corr = df.corr()

	sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
	plt.show()

def loadData():
	train_data = np.load("trainingData.npy")
	train_labels = np.load("trainingLabels.npy")

	test_data = np.load("testingData.npy")
	test_labels = np.load("testingLabels.npy")

	train_data = train_data / train_data.max()
	test_data = test_data / test_data.max()

	return train_data, train_labels, test_data, test_labels


def predAlg():

	# load data
	train_data, train_labels, test_data, test_labels = loadData()

	# classNames is the number of people that we believe are on the wifi
	classNames = []

	# the capacity of the building
	capacity = 50

	for i in range(0,capacity):
		classNames.append(i)	#these are your possible outputs (number of devices on the wifi

	model = keras.Sequential([
		#keras.layers.Flatten(input_shape=(NUM_ATTRIBUTES,1)), you probably don't need this line bc your input data for each hour is already flat (aka one of your dims is 1)
		keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(5,)), #64 was basically a random number for me. I'd experiment with bigger and smaller
		keras.layers.Dropout(0.1),		#makes sure you aren't overfitting and killing your test accuracy. This is a pretty high dropout rate, so make lower as needed (esp if you need a bigger training set)
		keras.layers.Dense(capacity + 1, activation=tf.nn.relu) #number of neurons in final layer should equal number of classes
	])

	# if changes are going to be made to increase accuracy it should be done here
	model.compile(optimizer='adam',loss=losses.mean_squared_error, metrics=['accuracy'])

	#more epochs = more work training ~= higher accuracy
	model.fit(train_data, train_labels, epochs=100, verbose=1)

	#for making re-running faster, toggle this to re-run with the same weights from the previous run
	model.save_weights("./checkpoints/weights")
	#model.load_weights works in reverse)

	# plot_model(model, to_file='model.png')

	test_loss, test_acc = model.evaluate(test_data, test_labels)

	print('Test accuracy:', test_acc)

if __name__ == '__main__':
	vis()
