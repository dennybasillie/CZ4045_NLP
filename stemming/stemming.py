import os
import operator
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import *

fileDir = os.path.dirname(os.path.realpath('_file_'))
dataLocation = os.path.join(fileDir, 'posts.txt')


def main():
    origFileHandler = open(dataLocation, "r")
    origTokensList = word_tokenize(origFileHandler.read())
    origWordCountDict = countWords(origTokensList)

    print "Top 20 Original:"
    origTopTwentyList = getTopTwenty(origWordCountDict)
    for tuple in origTopTwentyList:
        print tuple
    print("\n")

    stemmedDataLocation = os.path.splitext(dataLocation)[0] + "_stem.txt"
    stemFileHandler = open(stemmedDataLocation, 'w+')
    stemDerivativesDict = getStems(origTokensList, stemFileHandler)

    stemFileHandler.seek(0)
    stemTokensList = word_tokenize(stemFileHandler.read())
    stemWordCountDict = countWords(stemTokensList)
    print "Top 20 Stemmed:"
    stemTopTwentyList = getTopTwenty(stemWordCountDict)
    for tuple in stemTopTwentyList:
        print tuple,
        stem = tuple[0]
        print "=> " + " ".join(stemDerivativesDict[stem])
    print("\n")

    origFileHandler.close()
    stemFileHandler.close()

def getStems(wordList, outputFileHandler):
    stemmer = PorterStemmer()
    stemDerivativesDict = {}

    for word in wordList:
        wordLower = word.lower()
        stemmedWord = stemmer.stem(wordLower)
        outputFileHandler.write(stemmedWord + " ")
        if stemmedWord not in stemDerivativesDict:
            stemDerivativesDict[stemmedWord] = []
            stemDerivativesDict[stemmedWord].append(wordLower)
        else:
            if wordLower not in stemDerivativesDict[stemmedWord]:
                stemDerivativesDict[stemmedWord].append(wordLower)
    return stemDerivativesDict

def countWords(wordList):
    wordCount = {}
    stops = stopwords.words('english')
    for word in wordList:
        #Do not include anything that does not contain a word character
        if not re.match('^[\W]*$', word):
            wordLower = word.lower()
            if wordLower not in stops:
                if wordLower not in wordCount:
                    wordCount[wordLower] = 1
                else:
                    wordCount[wordLower] = wordCount[wordLower] + 1
    return wordCount

def getTopTwenty(wordCountDict):
    sortedWordCountList = sorted(wordCountDict.items(), key=operator.itemgetter(1), reverse=True)
    topTwentyList = []
    for index in range(0,20):
        topTwentyList.append(sortedWordCountList[index])
    return topTwentyList

if __name__ == '__main__':
    main()

