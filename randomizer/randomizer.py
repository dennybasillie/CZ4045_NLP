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
questionLocation = os.path.join(fileDir, 'questions-cleaned.txt')
answerLocation = os.path.join(fileDir, 'answers-cleaned.txt')

threadAmount = 100
thread_output = open('random-threads.txt', 'w')
question_output = open('random-questions.txt', 'w')
answer_output = open('random-answers.txt', 'w')

with open(questionLocation, 'r') as questionDicts, open(answerLocation, 'r') as answerDicts:
    questions = questionDicts.readlines()
    answers = answerDicts.readlines()
    question_amount = len(questions)
    counter = 0

    index_set = set()
    while len(index_set) < threadAmount:
        index_set.add(random.randrange(0, question_amount))

    for index in index_set:
        counter += 1
        question = eval(questions[index])
        thread_output.write('Thread-' + str(counter) + '\n\n')
        text = 'Question-' + str(question['questionId']) + '\n'
        thread_output.write('       ' + text)
        question_output.write(text)
        text = str(question['question']) + '\n'
        thread_output.write('       ' + text)
        question_output.write(text)
        thread_output.write('\n')
        question_output.write('\n')

        # The answers are sorted by questionId, so the answers for the same question is located in series.
        # If the series broke, there is no need to go through the next answers.
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
                text = 'Answer-' + str(answer['answerId'])
                thread_output.write('               ' + text + '\n')
                answer_output.write(text + ', Question-' + answer['questionId'] + '\n')
                text = str(answer['answer']) + '\n\n'
                thread_output.write('               ' + text)
                answer_output.write(text)


thread_output.close()
question_output.close()
answer_output.close()

# Delete the extra empty lines at the end of the output files.
delete_last_empty_lines('random-threads.txt')
delete_last_empty_lines('random-questions.txt')
delete_last_empty_lines('random-answers.txt')