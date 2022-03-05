import argparse
import sys

from baseline import baseline
from viterbi_1 import viterbi_1
from viterbi_2 import viterbi_2
from viterbi_3 import viterbi_3

import utils

"""
This file contains the main application that is run for this MP.
"""


def main(args):
    print("Loading dataset...")
    train_set = utils.load_dataset(args.training_file)
    test_set = utils.load_dataset(args.test_file)
    print("Loaded dataset")
    print()

    algorithms = {"baseline": baseline, "viterbi_1": viterbi_1, "viterbi_2": viterbi_2, "viterbi_3": viterbi_3}
    algorithm = algorithms[args.algorithm]
    
    print("Running {}...".format(args.algorithm))
    testtag_predictions = algorithm(train_set, utils.strip_tags(test_set))
    baseline_acc, correct_wordtagcounter, wrong_wordtagcounter = utils.evaluate_accuracies(testtag_predictions,
                                                                                           test_set)
    multitags_acc, unseen_acc, = utils.specialword_accuracies(train_set, testtag_predictions, test_set)

    print("Accuracy: {:.2f}%".format(baseline_acc * 100))
    print("\tMultitags Accuracy: {:.2f}%".format(multitags_acc * 100))
    print("\tUnseen words Accuracy: {:.2f}%".format(unseen_acc * 100))
    print("\tTop K Wrong Word-Tag Predictions: {}".format(utils.topk_wordtagcounter(wrong_wordtagcounter, k=4)))
    print("\tTop K Correct Word-Tag Predictions: {}".format(utils.topk_wordtagcounter(correct_wordtagcounter, k=4)))
    
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS440 MP4 HMM')
    parser.add_argument('--train', dest='training_file', type=str,
                        help='the file of the training data')
    parser.add_argument('--test', dest='test_file', type=str,
                        help='the file of the testing data')
    parser.add_argument('--algorithm', dest='algorithm', type=str, default="baseline",
                        help='which algorithm to run: baseline, viterbi_1, viterbi_2, viterbi_3')
    args = parser.parse_args()
    if args.training_file == None or args.test_file == None:
        sys.exit('You must specify training file and testing file!')

    main(args)
