import os
import re
import sys
import time
import math
import random

def main():
    if (len(sys.argv) < 2):
        print("To use: python k_fold_preprocessor.py [conll_file_path_1, conll_file_path_2, ...]")
        return

    post_file_name_list = sys.argv[1:]
    post_list = []
    for post_file_name in post_file_name_list:
        post = []
        with open(post_file_name, mode='r') as conll_path:
            file_contents = list(filter('\n'.__ne__, conll_path.readlines()))
            for i in range(len(file_contents)):
                line = file_contents[i].strip()
                label, _, _, token = line.split('\t')
                #remove post number, question number, and answer number
                if label == 'O':
                    continue
                #indicate B-token or I-token as Token
                if label == 'B-Token' or label == 'I-Token':
                    label = 'Token'
                post.append((token, label))
        print(len(post))
        post_list.append(post)
    
    for i in range(len(post_file_name_list)):
        train_list = post_list[:i] + post_list[i+1:]
        test_list = post_list[i:i+1]

        with open('train-%d.txt' % (i+1), mode='w') as train_file, open('test-%d.txt' % (i+1), mode='w') as test_file:
            for post in train_list:
                for token, name_entity in post:
                    train_file.write('%s\t%s\n' % (token, name_entity))
            for post in test_list:
                for token, name_entity in post:
                    test_file.write('%s\t%s\n' % (token, name_entity))

if __name__ == '__main__':
    main()


