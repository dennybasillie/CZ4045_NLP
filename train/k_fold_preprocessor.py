import os
import re
import sys
import time
import math
import random

post_dir = '../annotation-util' 
post_file_name_list = ['Post-1', 'Post-2', 'Post-3', 'Post-4']
post_conll_list = ['Post-1-irregular.conll', 'Post-2-irregular.conll', 'Post-3-irregular.conll', 'Post-4-irregular.conll']
k = 4

def main():
    post_list = []
    for post_file_name in post_file_name_list:
        print(post_file_name)
        full_path = os.path.join(post_dir, post_file_name+"-irregular.conll")
        post = []
        with open(full_path, mode='r') as conll_path:
            file_contents = list(filter('\n'.__ne__, conll_path.readlines()))
            print(len(file_contents))
            for i in range(len(file_contents)):
                line = file_contents[i].strip()
                label, _, _, token = line.split('\t')
                if label == 'O':
                    continue
                post.append((token, label))
        print(len(post))
        post_list.append(post)
    
    for i in range(k):
        train_list = post_list[:i] + post_list[i+1:]
        test_list = post_list[i:i+1]

        with open('train-%d.txt' % i, mode='w') as train_file, open('test-%d.txt' % i, mode='w') as test_file:
            for post in train_list:
                for token, name_entity in post:
                    train_file.write('%s\t%s\n' % (token, name_entity))
            for post in test_list:
                for token, name_entity in post:
                    test_file.write('%s\t%s\n' % (token, name_entity))

if __name__ == '__main__':
    main()


