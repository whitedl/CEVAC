from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import keras
# from tensorflow.keras.callbacks import EarlyStopping
from keras import losses
from keras.utils import plot_model
from keras.layers import Dense, Activation, Dropout, Conv1D
from keras.callbacks import EarlyStopping

# Helper libraries
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import os

# read in our data
def loadData():

	train_data = np.load('powerTrainingData.npy')
	train_labels = np.load('powerTrainingLabels.npy')

	test_data = np.load('powerTestingData.npy')
	test_labels = np.load('powerTestingLabels.npy')

	return train_data, train_labels, test_data, test_labels

# prediction with the built-in keras model
def createModel(opt, length):

	# create the keras instance
	model = keras.Sequential()

	# add layers
	model.add(Dense(100, input_shape=(length,)))
	model.add(Activation('sigmoid'))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(optimizer=opt,loss=losses.mse, metrics=['accuracy'])

	return model

# trains the model
def train(model):
    # load data
    train_data, train_labels, test_data, test_labels = loadData()

    # stops the model when the loss is no longer decreasing
    early_stopping = EarlyStopping(monitor='loss', patience=5)

    #more epochs = more work training ~= higher accuracy
    model.fit(train_data, train_labels, epochs=50, verbose=1, callbacks=[early_stopping]) #

    # for making re-running faster, toggle this to re-run with the same weights from the previous run
    model.save_weights('powerModel.h5')
    # model.load_weights("./checkpoints/weights")	# works in reverse)

    test_loss, test_acc = model.evaluate(test_data, test_labels)

    print('Test accuracy:', test_acc)

def pred(model):

	model.load_weights('powerModel.h5')

	train_data, train_labels, test_data, test_labels = loadData()

	y = model.predict(test_data, verbose = 1)

	differences = []

	for i, element in enumerate(y):

		difference = element[0] - test_labels[i][0]
		differences.append(difference)

	print('STANDARD DEV:\t{}'.format(np.std(differences)))
	print('MEAN DIFFERENCE:\t{}'.format(np.mean(differences)))

if __name__ == '__main__':
	model = createModel('adam', 46)
	train(model)
	pred(model)
