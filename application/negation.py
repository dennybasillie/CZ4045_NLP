# The project application

import os
import re
import sys
from nltk.tokenize import sent_tokenize
import tokenizer_re

negationWords = ["not", "doesn't", "no", "don't", "never", "haven't", "can't", "isn't", "couldn't", "didn't", "shouldn't", "won't", "wasn't", "wouldn't", "aren't", "hasn't", "weren't", "arn't"]

def findNegation(tokens):
    for token in tokens:
        if token in negationWords:
            return True
    return False

def tokenizer(sent):
    with open('sent.txt', 'w') as f:
        f.write(sent)
    tokens = []
    tokenizer_re.main("sent")
    with open('sent.ann', 'r') as f:
        for line in f:
            m = re.search('(T\d+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(.+)', line)
            tokens.append(m.group(5))
    try:
        os.remove('sent.txt')
        os.remove('sent.ann')
    except OSError, e:
        print("Failed to remove by-products of script. Please delete them manually.")
        pass
    return tokens

def output(negSent):
    if isinstance(negSent, basestring):
        negSent = [negSent]
    with open('negativeExpSent.txt', 'w') as f:
        for sent in negSent:
            f.write("Sentence:\n" + sent + "\n\n")

def negationSingle(sent):
    tokens = tokenizer(sent)
    negative = findNegation(tokens)
    if negative:
        output(sent)
        print("The sentence contains negation expression.")
        print("It has been written to 'negativeExpSent.txt' in the same folder.")
        return
    print("The sentence does not contain any negation expression.")

def negationBatch(file):
    negativeExpSents = []
    with open(file, 'r') as f:
        text = f.readlines()
    for line in text:
        sents = sent_tokenize(line)
        for sent in sents:
            if sent == "":
                continue
            tokens = tokenizer(sent)
            for token in tokens:
                if token in negationWords and sent not in negativeExpSents:
                    negativeExpSents.append(sent)

    output(negativeExpSents)
    print('Number of sentences with negative expressions detected: %d'%len(negativeExpSents))
    print("All the sentences have been written to 'negativeExpSent.txt' in the same folder.")

def main(file):
    negationBatch(file)

if __name__ == "__main__":
	main(sys.argv[1])