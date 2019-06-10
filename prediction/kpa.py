from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from keras import losses
from tensorflow.keras.callbacks import EarlyStopping
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

class SimpleMLP(keras.Model):

    def __init__(self, use_bn=False, use_dp=False, num_classes=300):
        super(SimpleMLP, self).__init__(name='mlp')
        self.use_bn = use_bn
        self.use_dp = use_dp
        self.num_classes = num_classes

        self.dense1 = keras.layers.Dense(512, activation='relu')
        # self.dense2 = keras.layers.Dense(256, activation='relu')
        self.dense2 = keras.layers.Dense(num_classes, activation='softmax')
        if self.use_dp:
            self.dp = keras.layers.Dropout(0.35)
        if self.use_bn:
            self.bn = keras.layers.BatchNormalization(axis=-1)

    def call(self, inputs):
        x = self.dense1(inputs)
        if self.use_dp:
            x = self.dp(x)
        if self.use_bn:
            x = self.bn(x)
        return self.dense2(x)


# read in our data
def loadData():

	train_data = np.load("powerTrainingData.npy")
	train_labels = np.load("powerTrainingLabels.npy")

	test_data = np.load("powerTestingData.npy")
	test_labels = np.load("powerTestingLabels.npy")

	train_data = train_data / train_data.max()
	test_data = test_data / test_data.max()

	return train_data, train_labels, test_data, test_labels

# use our custom keras model
def customAlg():

	# make a model instanace
	model = SimpleMLP()
	# stops the model when the loss is no longer decreasing
	model.compile(optimizer='adam',loss=losses.categorical_crossentropy, metrics=['accuracy'])
	return model

# prediction with the built-in keras model
def predAlg(buildingOccupancy):
	# the capacity of the building
	class_names = [i for i in range(0,buildingOccupancy)]	#these are your possible outputs (number of devices on the wifi

	# create the keras instance
	model = keras.Sequential([
		keras.layers.Dense(256, activation=tf.nn.relu), #64 was basically a random number for me. I'd experiment with bigger and smaller
		keras.layers.Dropout(0.25),		# makes sure you aren't overfitting and killing your test accuracy. This is a pretty high dropout rate, so make lower as needed (esp if you need a bigger training set)
		keras.layers.Dense(buildingOccupancy, activation=tf.nn.relu) #number of neurons in final layer should equal number of classes
	])

	# if changes are going to be made to increase accuracy it should be done here
	model.compile(optimizer='sgd',loss=losses.categorical_crossentropy, metrics=['accuracy'])
	return model

def train(model):

	# load data
	train_data, train_labels, test_data, test_labels = loadData()

	# stops the model when the loss is no longer decreasing
	early_stopping = EarlyStopping(monitor='loss', patience=500)

	#more epochs = more work training ~= higher accuracy
	model.fit(train_data, train_labels, epochs=10000, verbose=0, callbacks=[early_stopping])

	# for making re-running faster, toggle this to re-run with the same weights from the previous run
	model.save_weights("./checkpoints/weights")
	# model.load_weights("./checkpoints/weights")	# works in reverse)

	test_loss, test_acc = model.evaluate(test_data, test_labels)

	print('Test accuracy:', test_acc)

if __name__ == '__main__':
	train(customAlg())
