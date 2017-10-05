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
questionLocation = os.path.join(fileDir, '../preprocessing/questions-cleaned.txt')
answerLocation = os.path.join(fileDir, '../preprocessing/answers-cleaned.txt')

post_amount = 100
post_output = open('random-posts.txt', 'w')

with open(questionLocation, 'r') as questionDicts, open(answerLocation, 'r') as answerDicts:
    questions = questionDicts.readlines()
    answers = answerDicts.readlines()
    question_amount = post_amount / 2
    answer_amount = post_amount - question_amount
    total_question = len(questions)
    total_answer = len(answers)

    counter = 0;

    index_set = set()
    while len(index_set) < question_amount:
        index_set.add(random.randrange(0, total_question))

    for index in index_set:
        counter += 1
        question = eval(questions[index])
        text = 'Post-' + str(counter) + ', Question-' + str(question['questionId']) + '\n'
        post_output.write(text)
        text = str(question['question']) + '\n'
        post_output.write(text)
        post_output.write('\n')

    index_set = set()
    while len(index_set) < answer_amount:
        index_set.add(random.randrange(0, total_answer))

    for index in index_set:
        counter += 1
        answer = eval(answers[index])
        text = 'Post-' + str(counter) + ', Answer-' + str(answer['answerId']) +  ', Question-' + str(answer['questionId']) + '\n'
        post_output.write(text)
        text = str(answer['answer']) + '\n'
        post_output.write(text)
        post_output.write('\n')

post_output.close()

# Delete the extra empty lines at the end of the output files.
delete_last_empty_lines('random-posts.txt')