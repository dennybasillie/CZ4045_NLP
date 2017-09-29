import os

import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import *

fileDir = os.path.dirname(os.path.realpath('_file_'))
questionLocation = os.path.join(fileDir, '../preprocessing/questions-cleaned.txt')
answerLocation = os.path.join(fileDir, '../preprocessing/answers-cleaned.txt')

posts = []
temp = {}
with open(questionLocation) as question, open(answerLocation) as answer:
    while len(posts) < 5:
        for line in question:
            temp = eval(line)

            sentences = sent_tokenize(temp['question'])

            # Remove sentences with awkward newline characters (because of code section removal)
            posts += [sentence for sentence in sentences if not '\n' in sentence]

    # Only 5 sentences from question, 5 sentences from answer
    while len(posts) > 5:
        del posts[-1]

    while len(posts) < 10:
        for line in answer:
            temp = eval(line)

            sentences = sent_tokenize(temp['answer'])

            # Remove sentences with awkward newline characters (because of code section removal)
            posts += [sentence for sentence in sentences if not '\n' in sentence]

    # Delete excess posts
    while len(posts) > 10:
        del posts[-1]

output = open("postagged-sents.txt", "w")

for i in range(0, 10):
    output.write('Sentence ' + str(i+1) + ": " + posts[i])
    output.write('\n')
    output.write(str(nltk.pos_tag(word_tokenize(posts[i]))))
    if i != 9:
        output.write('\n\n')

output.close()