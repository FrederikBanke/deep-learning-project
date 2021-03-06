import numpy as np
import math
from keras.utils import Sequence, conv_utils
from keras import initializers, activations, regularizers
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
import os
from keras.utils import np_utils
import random


# Here, `x_set` is list of path to the images
# and `y_set` are the associated classes.
def search(directory, data, labels, label):
    i = 0
    for filename in os.listdir(directory):
        if i % 200 == 0:
            print(i)
        i = i + 1
        if filename.endswith(".jpeg"):
            img = load_img(
                directory + filename, grayscale=True, target_size=(224, 224),
            )
            img_array = img_to_array(img)
            data.append(img_array)
            labels.append(label)
        elif filename.endswith(".txt"):
            # filename.readLline()
            matrix = np.expand_dims(np.genfromtxt(directory + filename), axis=-1)
            data.append(matrix)
            labels.append(label)


class mySequence(Sequence):
    def __init__(self, directory, batch_size):
        self.batch_size = batch_size
        self.director = directory
        self.data = []
        self.labels = []
        search(directory + "/NORMAL/", self.data, self.labels, 0)
        search(directory + "/PNEUMONIA/", self.data, self.labels, 1)
        # shuffle at the beginning
        tmp = list(zip(self.data, self.labels))
        random.shuffle(tmp)
        self.data, self.labels = zip(*tmp)

        self.data = np.asarray(self.data)
        self.labels = np.asarray(self.labels)
        self.data = self.data / 255.0
        self.labels = np_utils.to_categorical(self.labels)

    def __len__(self):
        return math.ceil(len(self.data) / self.batch_size)

    def __getitem__(self, idx):

        return (
            self.data[idx * self.batch_size : (idx + 1) * self.batch_size],
            self.labels[idx * self.batch_size : (idx + 1) * self.batch_size],
        )
