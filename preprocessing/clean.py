import os

from bs4 import BeautifulSoup

fileDir = os.path.dirname(os.path.realpath('_file_'))
questionLocation = os.path.join(fileDir, '../dataset/questions.txt')
answerLocation = os.path.join(fileDir, '../dataset/answers.txt')

temp = {}

with open(questionLocation, 'r') as input, open('questions-cleaned.txt', 'w') as output:
    lines = input.readlines()
    numberOfLines = len(lines)
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
        temp.update({'question' : soup.text})
        output.write(str(temp))

        if counter != numberOfLines:
            output.write('\n')

with open(answerLocation, 'r') as input, open('answers-cleaned.txt', 'w') as output:
    lines = input.readlines()
    numberOfLines = len(lines)
    counter = 0

    for line in lines:
        counter += 1
        temp = eval(line)
        soup = BeautifulSoup(temp['answer'], 'html.parser')

        # Remove any code sections
        codeSents = soup.find_all('pre')
        for codeSent in codeSents:
            codeSent.extract()

        # soup.text returns clean text, free from html tags
        temp.update({'answer': soup.text})
        output.write(str(temp))

        if counter != numberOfLines:
            output.write('\n')