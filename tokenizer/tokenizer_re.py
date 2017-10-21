import nltk
import os
import re
import sys



def main():
    test_list = ["@User Name", "http://www.google.com", "/var/folder/file.sh", "Java 7", "non-generic", "I'm", "int indexOf()",
                 "int indexOf(string mystring)", "this is an (example legit sentence)", "another(legit sentence)", ":)",
                 "java.utils.collections", "Class<E>", "Jon Snow", "CATALINA_OPTS=\"$CATALINA_OPTS -Xms512m\"",
                 "CATALINA_OPTS=\"$CATALINA_OPTS -xx:MaxPermSize=25m\"", "1)", "2)"]

    # for test in test_list:
    #     print nltk.tokenize.word_tokenize(test)

    fileName = sys.argv[1]
    txtFileLocation = fileName + ".txt"
    annFileLocation = fileName + ".ann"
    with open(txtFileLocation, 'r') as txtFileHandler, open(annFileLocation, 'w+') as annFileHandler:
        processedLength = 0
        tokenId = 1
        tokenName = "Token"

        #http, directory, package name / file name, function call, template, number list, word with - or ' in the middle, a word, single symbol
        regex = r"https?://.*|^(/\w+)+(\.\w+|/)?|\w+(\.\w+)+|\w+\(\)|[A-Z][\w_]*<[A-Z][\w_]*>|^\d+\)|\w+([-']?\w+)*|\w+|\W"

        # for line in txtFileHandler:
        for line in test_list:
            if line.strip() and not re.match("^Post-(\d)+.*Question-(\d)+$", line):
                wordList, indexList = zip(*[(m.group(0), (m.start(), m.end())) for m in re.finditer(r'\S+', line)])

                #Handle multi-word tokens

                #Handle single-word tokens
                for (word,index) in zip(wordList, indexList):
                    matches = [(n.group(0), (n.start(), n.end())) for n in re.finditer(regex, word)]
                    if matches:
                        subwordList, subindexList = zip(*matches)
                        for (subword, subindex) in zip(subwordList, subindexList):
                            print (
                                "T" + str(tokenId) + "\t" + tokenName + " " + str(
                                    processedLength + index[0] + subindex[0]) + " " + str(
                                    processedLength + index[0] + subindex[1]) + "\t" + subword + "\n")
                            tokenId += 1

            #Move to the next line, increment pointer
            processedLength += len(line)


if __name__ == '__main__':
    main()
