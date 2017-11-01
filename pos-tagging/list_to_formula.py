# -*- coding: utf-8 -*-

# Convert the tagged sentence list to Word formula linear format.
# When you convert linear format to professional format in Word,
# there will be problem while converting '(' and ')' characters.

import ast
import sys

if (len(sys.argv) < 2):
    print("To use: python list_to_formula.py filename(with extension)")
    exit()
fileName = sys.argv[1]

with open(fileName, 'r') as input, open('postagged-formula.txt', 'w') as output:
    for line in input.readlines():
        if line[0] != "[":
            continue
        tag_list = ast.literal_eval(line)

        result = ''
        for item in tag_list:
            result += '⏟(' + item[0] + ')_' + item[1] + '   '

        output.write(result + '\n')