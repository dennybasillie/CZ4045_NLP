import os
import re
import sys
import enchant
import operator

def main():
    fileName = sys.argv[1]
    # outputLocation = os.path.splitext(fileLocation)[0] + ".ann"
    with open(fileName, 'r+') as annFileHandler:
        dict = enchant.Dict("en_US")
        wordCount = {}

        for line in annFileHandler:
            m = re.search('(T\d+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(.+)', line)  # token_id, token_name, start, end, token
            token = m.group(5)
            print ("Token: " + token)
            if not dict.check(token) and not re.search('^\W+$', token):
                print ("Non-standard token found: " + token)
                wordLower = token.lower()
                if wordLower not in wordCount:
                    wordCount[wordLower] = 1
                else:
                    wordCount[wordLower] = wordCount[wordLower] + 1

        print ("\n")
        sortedWordCountList = sorted(wordCount.items(), key=operator.itemgetter(1), reverse=True)
        topTwentyList = []
        for index in range(0, 20):
            topTwentyList.append(sortedWordCountList[index])
        print "Top 20 Non-standard English word:"
        for tuple in topTwentyList:
            print (tuple)



if __name__ == '__main__':
    main()