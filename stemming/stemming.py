import os
import operator
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import *

fileDir = os.path.dirname(os.path.realpath('_file_'))
questionLocation = os.path.join(fileDir, "..", "preprocessing", "questions-cleaned.txt")
answerLocation = os.path.join(fileDir, "..", "preprocessing", "answers-cleaned.txt")
stopwordsLocation = os.path.join(fileDir, "stopwords.txt")

def main():
    #Parse questions and answers into single combined string
    strPosts = ' '.join(combineQuestionsAndAnswers())

    #Parse stopwords.txt into a list of stopwords
    stopwordList = []
    with open(stopwordsLocation, 'r') as stopwordsFileHandler:
        stopwordList = stopwordsFileHandler.readlines()
    stopwordList = [stopword.strip() for stopword in stopwordList]

    #Tokenize the string of questions and answers, and count occurences of non-stopwords
    origTokensList = word_tokenize(strPosts)
    origWordCountDict = countWords(origTokensList, stopwordList)

    #Print out top 20 frequent words and their occurence counts
    print "Top 20 Original:"
    origTopTwentyList = getTopTwenty(origWordCountDict)
    for tuple in origTopTwentyList:
        print tuple
    print("\n")

    #Stem the questions and answers, and output as a single file
    stemTokensList, stemOriginalsDict = getStems(origTokensList)

    #Create a list of stemmed stopwords
    stemStopwordsList, stemStopwordsOriginalsDict = getStems(stopwordList)

    #Print out top 20 frequent stemmed words, their occurence counts, and their original words
    stemWordCountDict = countWords(stemTokensList, stemStopwordsList)
    print "Top 20 Stemmed:"
    stemTopTwentyList = getTopTwenty(stemWordCountDict)
    for tuple in stemTopTwentyList:
        print tuple,
        stem = tuple[0]
        print "=> " + " ".join(stemOriginalsDict[stem])
    print("\n")

def combineQuestionsAndAnswers():
    posts = []
    with open(questionLocation, 'r') as questionFileHandler, open(answerLocation, 'r') as answerFileHandler:
        for line in questionFileHandler:
            temp = eval(line)
            sentences = sent_tokenize(temp['question'].encode('ascii', 'ignore'))

            # Remove sentences with awkward newline characters (because of code section removal)
            posts += [sentence for sentence in sentences if not '\n' in sentence]

        for line in answerFileHandler:
            temp = eval(line)
            sentences = sent_tokenize(temp['answer'].encode('ascii', 'ignore'))

            # Remove sentences with awkward newline characters (because of code section removal)
            posts += [sentence for sentence in sentences if not '\n' in sentence]

    return posts

def getStems(wordList):
    stemmer = PorterStemmer()
    stemDerivativesDict = {}
    stemWordsList = []

    for word in wordList:
        wordLower = word.lower()
        stemmedWord = stemmer.stem(wordLower).encode('ascii', 'ignore')
        stemWordsList.append(stemmedWord)
        if stemmedWord not in stemDerivativesDict:
            stemDerivativesDict[stemmedWord] = []
            stemDerivativesDict[stemmedWord].append(wordLower)
        else:
            if wordLower not in stemDerivativesDict[stemmedWord]:
                stemDerivativesDict[stemmedWord].append(wordLower)
    return stemWordsList, stemDerivativesDict

def countWords(wordList, stopwordList):
    wordCount = {}
    nltkStopwords = stopwords.words('english')
    for word in wordList:
        #Do not include anything that only contains symbols (non-word characters)
        if not re.match('^[\W]*$', word):
            wordLower = word.lower()
            if (wordLower not in nltkStopwords) and (wordLower not in stopwordList):
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

