import os
import operator
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

fileDir = os.path.dirname(os.path.realpath('_file_'))
dataLocation = os.path.join(fileDir, 'posts.txt')

def main():
    origFileHandler = open(dataLocation, "r")
    origWordCount = countWords(origFileHandler)
    print "Top 20 Original:\n_______________________________"
    origTopTwentyList = getTopTwenty(origWordCount)
    for tuple in origTopTwentyList:
        print tuple
    print("\n")

    origFileHandler.seek(0)
    stemmedDataLocation = os.path.splitext(dataLocation)[0] + "_stem.txt"
    stemFileHandler = open(stemmedDataLocation, 'w+')

    stemDerivativesDict = getStems(origFileHandler, stemFileHandler)
    stemFileHandler.seek(0)
    stemWordCount = countWords(stemFileHandler)
    print "Top 20 Stemmed:\n_______________________________"
    stemTopTwentyList = getTopTwenty(stemWordCount)
    for tuple in stemTopTwentyList:
        print tuple
    print("\n")

    getOriginalsFromStems(stemDerivativesDict, stemTopTwentyList)

    origFileHandler.close()
    stemFileHandler.close()

def getOriginalsFromStems(stemDerivativesDict, stemTopTwentyList):
    print "Stems : Originals\n_______________________________"
    for topStemTuple in stemTopTwentyList:
        topStem = topStemTuple[0]
        print topStem + " : " + " ".join(stemDerivativesDict[topStem])

def getStems(inputFileHandler, outputFileHandler):
    stemmer = PorterStemmer()
    stemDerivativesDict = {}

    stemmedDataLocation = os.path.splitext(dataLocation)[0] + "_stem.txt"
    stemFileHandler = open(stemmedDataLocation, 'w')

    for line in inputFileHandler:
        for word in line.split():
            wordLower = word.lower()
            stemmedWord = stemmer.stem(wordLower)
            outputFileHandler.write(stemmedWord + " ")
            if stemmedWord not in stemDerivativesDict:
                stemDerivativesDict[stemmedWord] = []
                stemDerivativesDict[stemmedWord].append(wordLower)
            else:
                if wordLower not in stemDerivativesDict[stemmedWord]:
                    stemDerivativesDict[stemmedWord].append(wordLower)
        outputFileHandler.write("\n")
    return stemDerivativesDict

def countWords(fileHandler):
    wordCount = {}
    stops = stopwords.words('english')
    for line in fileHandler:
        for word in line.split():
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

