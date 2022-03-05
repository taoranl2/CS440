# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""

import numpy as np

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    b = 0
    W = np.zeros(train_set.shape[1])

    for i in range(max_iter):
        for j in range (len(train_set)):
            calculate = np.sign(np.dot(W, train_set[j]) + b)
            label = train_labels[j]
            if label != 0:
                revised_lable = label
            else:
                revised_lable = -1
            if calculate != revised_lable:
                W += learning_rate * revised_lable * train_set[j]
                b += learning_rate * revised_lable
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W,b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    result = []
    animal = 1
    non_animal = 0
    for i in dev_set:
        if np.sign(np.dot(W, i) + b) > 0:
            result.append(animal)
        else:
            result.append(non_animal)
    return result

def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here
    result = []
    animal = 1
    non_animal = 0
    for i in dev_set:
        knn_dict = {}
        for j in range(len(train_set)):
            dis = Euclidean_distance(i,train_set[j])
            if (len(knn_dict) == k):
                if (max(knn_dict.keys()) > dis):
                    knn_dict.pop(max(knn_dict.keys()))
                    knn_dict[dis] = train_labels[j]
            else:
                knn_dict[dis] = train_labels[j]
        if (sum(knn_dict.values()) <= k / 2):
            result.append(non_animal)
        else:
            result.append(animal)
    return result

def Euclidean_distance(matrix1, matrix2):
    sub = matrix1 - matrix2
    sub_square = np.square(sub)
    total_dis = np.sum(sub_square)
    return np.sqrt(total_dis)