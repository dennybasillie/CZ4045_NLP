import os

import sys
import nltk
import enchant
from nltk.tokenize import *
from random import randint

def main():
    fileName = sys.argv[1]

    outFile = "selected_irregular_posts.txt"

    selected_posts = []
    all_sentences = []
    with open(fileName, 'r+') as txtFileHandler:
        for line in txtFileHandler:
            sentences = sent_tokenize(line.encode('ascii', 'ignore'))
            for sentence in sentences:
                all_sentences.append(sentence)


    checked_index = []
    selected_sentences = []
    all_sentences_len = len(all_sentences)
    while len(selected_sentences) < 10:
        index = randint(0, all_sentences_len - 1)
        if (index not in checked_index):
            sentence = all_sentences[index]

            wordList, indexList = zip(*[(m.group(0), (m.start(), m.end())) for m in
                                        re.finditer(r'@?([A-Z]+\w+\s+)+(([A-Z]+\w+)|((\d+\.)*\d+))|\S+', sentence)])
            # Process each single-word tokens
            for (word, index) in zip(wordList, indexList):
                if re.search('^.+(\s+.+)+$', word) or (not re.search('^[-<\."\'\(-]*\w+([-\']?\w+)*[\W]*$', word) and not re.search('^\W+$', word)):
                   selected_sentences.append(sentence)
                   break

    index = 0
    for sentence in selected_sentences:
        index = index + 1
        with open(outFile, 'w') as outFileHandler:
            outFileHandler.write (sentence)
        cmd = "python ../tokenizer/tokenizer_re.py " + os.path.splitext(outFile)[0]
        os.system(cmd)

        tokens = []
        print ("Sentence " + str(index) + ": " + sentence + "\n")
        with open(os.path.splitext(outFile)[0] + ".ann", 'r') as annFileHandler:
            for line in annFileHandler:
                m = re.search('(T\d+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(.+)', line)  # token_id, token_name, start, end, token
                tokens.append(m.group(5))

        print (str(nltk.pos_tag(tokens)) + "\n")

if __name__ == '__main__':
    main()
