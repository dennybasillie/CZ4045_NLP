import nltk
import os
import re
import sys



def main():
    test_list = ["@User Name", "http://www.google.com", "name@email.com", "@myself", "/var/folder/file.sh", "Java 7", "non-generic", "I'm", "int indexOf()",
                 "int indexOf(string mystring)", "this is an (example legit sentence)", "another(legit sentence)", ":)",
                 "java.utils.collections", "Class<E>", "Bobby Goodfield Matthew", "CATALINA_OPTS=\"$CATALINA_OPTS -Xms512m\"",
                 "CATALINA_OPTS=\"$CATALINA_OPTS -xx:MaxPermSize=25m\"", "e.g.", ".NET", "end. A new", "end.A new", "Axis 1.4"]

    # for test in test_list:
    #     print nltk.tokenize.word_tokenize(test)

    fileName = sys.argv[1]
    txtFileLocation = fileName + ".txt"
    annFileLocation = fileName + ".ann"
    with open(txtFileLocation, 'r') as txtFileHandler, open(annFileLocation, 'w+') as annFileHandler:
        processedLength = 0
        tokenId = 1
        tokenName = "Token"

        #multi-word tokens, http, email, argument flags, dollar variables, one-word mentions(@), simple abbreviations (e.g., i.e.) directory, package name / file name, extensions / .NET, function call, template, word with - or ' in the middle, a word, single symbol
        regex = r".+(\s+.+)+|https?://.*|\w+@\w+(\.\w+)+|^--?\w+.+[^\"]|\$[\w_]+|^@\w+|([A-Za-z]\.){2,}|^(/\w+)+(\.\w+|/)?|\w+(\.\w+)+|^\.\w+|\w+\(\)|[A-Z][\w_]*<[A-Z][\w_]*>|\w+([-']?\w+)*|\w+|\W"

        for line in txtFileHandler:
        # for line in test_list:
            if line.strip() and not re.match("^Post-(\d)+.*Question-(\d)+$", line):
                #Get multi-words tokens and single-word tokens
                wordList, indexList = zip(*[(m.group(0), (m.start(), m.end())) for m in re.finditer(r'@?([A-Z]+\w+\s+)+(([A-Z]+\w+)|((\d+\.)*\d+))|\S+', line)])

                #Process each single-word tokens
                for (word,index) in zip(wordList, indexList):
                    matches = [(n.group(0), (n.start(), n.end())) for n in re.finditer(regex, word)]
                    if matches:
                        subwordList, subindexList = zip(*matches)
                        for (subword, subindex) in zip(subwordList, subindexList):
                            annFileHandler.write (
                                "T" + str(tokenId) + "\t" + tokenName + " " + str(
                                    processedLength + index[0] + subindex[0]) + " " + str(
                                    processedLength + index[0] + subindex[1]) + "\t" + subword + "\n")
                            tokenId += 1

            #Move to the next line, increment pointer
            processedLength += len(line)


if __name__ == '__main__':
    main()
