import os
import re

from bs4 import BeautifulSoup
from operator import itemgetter

fileDir = os.path.dirname(os.path.realpath('_file_'))
questionLocation = os.path.join(fileDir, '../dataset/questions.txt')
answerLocation = os.path.join(fileDir, '../dataset/answers.txt')

temp = {}

with open(questionLocation, 'r') as input, open('questions-cleaned.txt', 'w') as output:
    lines = input.readlines()
    numberOfQuestions = len(lines)
    counter = 0

    for line in lines:
        counter += 1
        temp = eval(line)
        soup = BeautifulSoup(temp['question'], 'html.parser')

        # Remove any code sections
        codeSents = soup.find_all('pre')
        for codeSent in codeSents:
            codeSent.extract()

        # soup.text returns clean text, free from html tags
        # Cleanup trailing spaces and newline characters
        cleanText = soup.text.encode('ascii', 'ignore')
        cleanText = re.sub(r'(\n)+', ' ', cleanText).rstrip()

        temp.update({'question': cleanText.encode('ascii', 'ignore')})
        output.write(str(temp))

        if counter != numberOfQuestions:
            output.write('\n')

answerDicts = []
with open(answerLocation, 'r') as input, open('answers-cleaned.txt', 'w') as output:
    lines = input.readlines()
    counter = 0

    for line in lines:
        temp = eval(line)
        soup = BeautifulSoup(temp['answer'], 'html.parser')

        # Remove any code sections
        codeSents = soup.find_all('pre')
        for codeSent in codeSents:
            codeSent.extract()

        # soup.text returns clean text, free from html tags
        # Cleanup trailing spaces and newline characters
        cleanText = soup.text
        cleanText = re.sub(r'(\n)+', ' ', cleanText).rstrip()

        temp.update({'answer': cleanText.encode('ascii', 'ignore')})
        answerDicts.append(temp)

    sortedAnswerDicts = sorted(answerDicts, key=itemgetter('questionId'))
    numberOfAnswers = len(sortedAnswerDicts)

    for answer in sortedAnswerDicts:
        counter += 1
        output.write(str(answer))
        if counter != numberOfAnswers:
            output.write('\n')