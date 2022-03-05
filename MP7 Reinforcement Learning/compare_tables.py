
import os 
import numpy as np 
import argparse


def compare_tables(my_checkpoint_path, ta_checkpoint_path):
    my_checkpoint = np.load(my_checkpoint_path)
    ta_checkpoint = np.load(ta_checkpoint_path)

    differences = my_checkpoint == ta_checkpoint
    are_same = np.all(differences)

    count = 0
    if not are_same:
        # find the locations where the arrays differ
        indx_diff = np.where(differences == False)
        location = []
        for i in range (np.shape(indx_diff)[1]):
            for j in range (np.shape(indx_diff)[0]):
                location.append(indx_diff[j][i])
            if my_checkpoint[tuple(location)] != ta_checkpoint[tuple(location)]:
                print ("\nAt : " + str(location) + " , the values are: ")
                print ("Your's: " + str(my_checkpoint[tuple(location)]))
                print ("Solution's: " + str(ta_checkpoint[tuple(location)]))
                count += 1
            location = []
    if not count:
        return True
    else:
        return False

    
def main():
    parser = argparse.ArgumentParser(description='CS440 MP7 Snake Table Comparator')

    parser.add_argument('--test', dest = 'test', type=int, required=True, help='local test number (either 1, 2, or 3)')
    parser.add_argument('--checkpoint', dest = 'checkpoint', type=str, required=True, help='path to checkpoint Q table')
    parser.add_argument('--checkpoint-n',  dest = 'checkpoint_n', type=str, required=True, help='path to checkpoint N table file')				

    args = parser.parse_args()

    if args.test in [1, 2, 3]:
        checkpoint_q = args.checkpoint 
        checkpoint_n = args.checkpoint_n

        ta_checkpoint_q = './data/checkpoint' + str(args.test) + '.npy'
        ta_checkpoint_n = './data/checkpoint' + str(args.test) + '_N.npy'

        if os.path.exists(checkpoint_q) and os.path.exists(checkpoint_n):  
            compare_tables(checkpoint_q, ta_checkpoint_q)
            compare_tables(checkpoint_n, ta_checkpoint_n)
        else: 
            print('Please specify a valid path to both saved tables.')

    else: 
        print('Please specify valid test number 1, 2, or 3. ')
    

if __name__ == "__main__":
    main()