import os
import random


def delete_last_empty_lines(filename):
    target = open(filename, 'r')

    lines = target.readlines()
    lines[-2] = lines[-2].strip('\n')
    lines[-1] = lines[-1].strip('\n')
    target.close()

    target = open(filename, 'w')
    target.writelines(lines)
    target.close()


fileDir = os.path.dirname(os.path.realpath('_file_'))
questionLocation = os.path.join(fileDir, '../../preprocessing/questions-cleaned.txt')
answerLocation = os.path.join(fileDir, '../../preprocessing/answers-cleaned.txt')

output = open('posts-cleaned.txt', 'w')

with open(questionLocation, 'r') as questionDicts, open(answerLocation, 'r') as answerDicts:
    questions = questionDicts.readlines()
    answers = answerDicts.readlines()
    question_amount = len(questions)
    counter = 0

    for index in range(question_amount):
        question = eval(questions[index])
        text = str(question['question']) + '\n'
        output.write(text + '\n')

        found = False
        for answer_str in answers:
            answer = eval(answer_str)
            if answer['questionId'] != question['questionId']:
                if found == True:
                    break
                else:
                    continue
            else:
                found = True
                text = str(answer['answer']) + '\n\n'
                output.write(text)

output.close()


# Delete the extra empty lines at the end of the output files.
delete_last_empty_lines('posts-cleaned.txt')
