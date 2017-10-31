import os
import sys
import re
import enchant

def main():
    if (len(sys.argv) < 2):
        print("To use: python annotate.py filename(without extension)")
        return
    fileName = sys.argv[1]
    annFileLocation = fileName + ".ann"
    # outputLocation = os.path.splitext(fileLocation)[0] + ".ann"
    dict_word = enchant.Dict("en_US")
    with open(annFileLocation, 'r+') as input, open(fileName + "-irregular.ann", 'w') as output:
        for line in input:
            split_line = line.split()
            token = ' '.join(split_line[4:])
            #if re.search('[\W_]', line.split()[-1]):
            if re.search('[\W_]', token) or not dict_word.check(token):
                output.write(line.replace('Token', 'Irregular'))
            else:
                output.write(line)


if __name__ == '__main__':
    main()
