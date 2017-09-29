import os

import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import *

fileDir = os.path.dirname(os.path.realpath('_file_'))
dataLocation = os.path.join(fileDir, '../posts.txt')

posts = []
temp = {}
with open(dataLocation) as inp:
    while len(posts) < 10:
        for line in inp:
            temp = eval(line)
            soup = BeautifulSoup(temp['questionText'], 'html.parser')

            # Remove any code sections
            codeSents = soup.find_all('pre')
            for codeSent in codeSents:
                codeSent.extract()

            sentences = sent_tokenize(soup.text)

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
    output.write('\n\n')