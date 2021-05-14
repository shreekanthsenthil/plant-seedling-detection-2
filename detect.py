import os
import shutil

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors
import random
import cv2
import pickle

from math import sqrt, floor
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf

def pre_processing_combined(img_array):
    img_array = np.rint(img_array)
    img_array = img_array.astype('uint8')

    value = 40
    hsv_img_brigthen = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv_img_brigthen)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv_brigthen = cv2.merge((h, s, v))
    result_brighten = cv2.cvtColor(final_hsv_brigthen, cv2.COLOR_HSV2RGB)
    result_brighten = cv2.GaussianBlur(result_brighten, (5,5), 0)

    hsv_img = cv2.cvtColor(result_brighten, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv_img, (24, 50, 0), (55, 255, 255))
    result = cv2.bitwise_and(result_brighten, result_brighten, mask=mask)
    # print(result)
    result= result.astype('float64')
    return result



def create_model():
    lenet_model = tf.keras.Sequential()

    lenet_model.add(tf.keras.layers.Conv2D(filters = 6, kernel_size = 5, strides = 1, activation='relu', input_shape = (150,150,3)))

    lenet_model.add(tf.keras.layers.MaxPooling2D(pool_size = 2, strides = 2))

    lenet_model.add(tf.keras.layers.Conv2D(filters = 16, kernel_size = 5, strides = 1, activation='relu', input_shape = (14,14,6)))

    lenet_model.add(tf.keras.layers.MaxPooling2D(pool_size = 2, strides = 2))

    lenet_model.add(tf.keras.layers.Flatten())

    lenet_model.add(tf.keras.layers.Dense(units=120, activation='relu'))

    lenet_model.add(tf.keras.layers.Dense(units=84, activation='relu'))

    lenet_model.add(tf.keras.layers.Dense(units=12, activation='softmax'))

    lenet_model.load_weights('../lenet_model.h5')
    return lenet_model

if __name__ == "__main__":
    lenet_model = create_model()

    testimage = cv2.imread("./test.png")
    testimage = cv2.cvtColor(testimage, cv2.COLOR_BGR2RGB)
    testimage = cv2.resize(testimage, (150, 150))
    testimage = pre_processing_combined(testimage)
    testimage = np.array(testimage)
    testimage = testimage/255
    # plt.imshow(testimage)
    testimage = np.reshape(testimage, (1,150,150,3))
    prediction = np.argmax(lenet_model.predict(testimage))
    print("%d" %(prediction))

