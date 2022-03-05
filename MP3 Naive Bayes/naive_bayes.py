# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
from re import L
from warnings import filterwarnings
import numpy as np
import math
from tqdm import tqdm
from collections import Counter
import reader

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

"""
  load_data calls the provided utility to load in the dataset.
  You can modify the default values for stemming and lowercase, to improve performance when
       we haven't passed in specific values for these parameters.
"""


def load_data(trainingdir, testdir, stemming=False, lowercase=False, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset(trainingdir, testdir, stemming, lowercase,
                                                                       silently)
    return train_set, train_labels, dev_set, dev_labels


# Keep this in the provided template
def print_paramter_vals(laplace, pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""


def naiveBayes(train_set, train_labels, dev_set, laplace=0.01, pos_prior=0.75, silently=False):
    # Keep this in the provided template

    print_paramter_vals(laplace, pos_prior)
    pos_word_dict, neg_word_dict = word_dict(train_set, train_labels)
    pos_log_prob_dict, pos_unknown_log_prob = dict_p(pos_word_dict, laplace)
    neg_log_prob_dict, neg_unknown_log_prob = dict_p(neg_word_dict, laplace)
    print(len(dev_set))

    yhats = []
    for doc in tqdm(dev_set):
        # print(doc)
        pos = math.log(pos_prior)
        neg = math.log(1 - pos_prior)

        for i in doc:
            if i in pos_word_dict:
                pos += pos_log_prob_dict[i]
            else:
                pos += pos_unknown_log_prob
            if i in neg_word_dict:
                neg += neg_log_prob_dict[i]
            else:
                neg += neg_unknown_log_prob

        yhats.append((pos > neg))
        # print(yhats)
    return yhats


# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace, bigram_laplace, bigram_lambda, pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.01, bigram_laplace=0.003, bigram_lambda=0.4, pos_prior=0.5, silently=False):

    print_paramter_vals_bigram(unigram_laplace, bigram_laplace, bigram_lambda, pos_prior)

    pos_dict_wb, neg_dis_wb = dict_w(train_set, train_labels)
    pos_dict_pb, pr_pos_dict_pb = dict_p(pos_dict_wb, bigram_laplace)
    neg_dict_pb, pr_neg_dict_pb = dict_p(neg_dis_wb, bigram_laplace)


    pos_dict_w, neg_dict_w = word_dict(train_set, train_labels)
    pos_dict_p, pr_pos_dict_p = dict_p(pos_dict_w, unigram_laplace)
    neg_dict_p, pr_neg_dict_p = dict_p(neg_dict_w, unigram_laplace)
    yhats = []
    for doc in tqdm(dev_set, disable=silently):
        pos_u = math.log(pos_prior)
        neg_u = math.log(1 - pos_prior)

        for i in doc:
            if i in pos_dict_w:
                pos_u += pos_dict_p[i]
            else:
                pos_u += pr_pos_dict_p
            if i in neg_dict_w:
                neg_u += neg_dict_p[i]
            else:
                neg_u += pr_neg_dict_p

        pos_b = math.log(pos_prior)
        neg_b = math.log(1 - pos_prior)
        for i in range(len(doc) - 1):
            if (doc[i], doc[i + 1]) in pos_dict_wb:
                pos_b += pos_dict_pb[(doc[i], doc[i + 1])]
            else:
                pos_b += pr_pos_dict_pb

            if (doc[i], doc[i + 1]) in neg_dis_wb:
                neg_b += neg_dict_pb[(doc[i], doc[i + 1])]
            else:
                neg_b += pr_neg_dict_pb

        pos_val = bigram_lambda * pos_b + (1 - bigram_lambda) * pos_u
        neg_val = bigram_lambda * neg_b + (1 - bigram_lambda) * neg_u

        yhats.append((pos_val > neg_val))
    return yhats


def word_dict(training_set, training_label):
    pos_dic_w = {}
    neg_dict_w = {}

    for i in range(len(training_label)):
        sentence = training_set[i]
        if training_label[i] == 1:
            for j in sentence:
                if j in pos_dic_w:
                    pos_dic_w[j] += 1
                else:
                    pos_dic_w[j] = 1
        else:
            for j in sentence:
                if j in neg_dict_w:
                    neg_dict_w[j] += 1
                else:
                    neg_dict_w[j] = 1
    return pos_dic_w, neg_dict_w


def dict_p(word_dict, laplace):
    pro_dict = {}
    word_n = 0
    dif_word_n = len(word_dict)

    for i in word_dict:
        word_n += word_dict[i]

    pro = laplace / (word_n + laplace * (dif_word_n + 1))

    for i in word_dict:
        log_prob = math.log(word_dict[i] * pro / laplace + pro)
        pro_dict[i] = log_prob

    return pro_dict, math.log(pro)


def dict_w(training_set, training_label):
    pos_dict_w = {}
    neg_dict_w = {}
    if len(training_set) < 5:
        print(training_set)
    if len(training_label) < 5:
        print(training_label)
    for i in range(len(training_label)):
        sen = training_set[i]
        if training_label[i] == 1:
            for j in range(len(sen) - 1):
                if (sen[j], sen[j + 1]) in pos_dict_w:
                    pos_dict_w[(sen[j], sen[j + 1])] += 1
                else:
                    pos_dict_w[(sen[j], sen[j + 1])] = 1
        else:
            for j in range(len(sen) - 1):
                if (sen[j], sen[j + 1]) in neg_dict_w:
                    neg_dict_w[(sen[j], sen[j + 1])] += 1
                else:
                    neg_dict_w[(sen[j], sen[j + 1])] = 1
    if len(pos_dict_w) < 5:
        print(pos_dict_w)
    if len(neg_dict_w) < 5:
        print(neg_dict_w)
    return pos_dict_w, neg_dict_w
