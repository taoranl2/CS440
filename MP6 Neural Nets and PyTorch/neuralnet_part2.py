# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques (jmc12) for the fall 2021 semester 

"""
This is the main entry point for MP3. You should only modify code
within this file and neuralnet_part1.py,neuralnet_leaderboard -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utils import get_dataset_from_arrays
from torch.utils.data import DataLoader

class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.

        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param yhat - an (N,out_size) Tensor
            @param y - an (N,) Tensor
            @return l(x,y) an () Tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension
        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size = out_size
        self.function = torch.nn.Sequential(nn.Conv2d(3, 32, 3),
                                            nn.ReLU(),
                                            nn.MaxPool2d(2, 2),
                                            nn.Conv2d(32, 32, 3),
                                            nn.ReLU(),
                                            nn.MaxPool2d(2, 2),
                                            nn.Conv2d(32, 32, 3),
                                            nn.ReLU(),
                                            nn.MaxPool2d(2),
                                            nn.Flatten(),
                                            nn.Linear(128, 120),
                                            nn.ReLU(),
                                            nn.Linear(120, 84),
                                            nn.ReLU(),
                                            nn.Linear(84, out_size))
        self.optimizer = optim.Adam(self.function.parameters(), lr=lrate)
        
    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """

        return self.function(x.reshape(x.shape[0],3,32,32))

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) for this batch as a float (scalar)
        """

        output = self.forward(x)
        self.optimizer.zero_grad()
        loss = self.loss_fn(output, y)
        loss.backward()
        self.optimizer.step()
        return loss.detach().cpu().numpy()

def fit(train_set,train_labels,dev_set,epochs,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param epochs: an int, the number of epochs of training
    @param batch_size: size of each batch to train on. (default 100)

    This method _must_ work for arbitrary M and N.

    The model's performance could be sensitive to the choice of learning rate.
    We recommend trying different values in case your first choice does not seem to work well.

    @return losses: list of total loss at the beginning and after each epoch.
            Ensure that len(losses) == epochs.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """
    pro_set = get_dataset_from_arrays(train_set, train_labels)
    load = DataLoader(pro_set, batch_size=batch_size)
    net = NeuralNet(0.00042, torch.nn.CrossEntropyLoss(), 3072, 4)
    losses = []
    for i in range(epochs):
        loss = 0.0
        for j in load:
            x = j['features']
            y = j['labels']
            loss += net.step(x, y)
        # print("epoch:", i, "loss:", loss)
        losses.append(loss)
    return losses, torch.argmax(net(dev_set), dim=1).detach().cpu().numpy().astype(int), net