import os
import sys
import re

def main():
    if (len(sys.argv) < 2):
        print("To use: python annotate.py filename(without extension)")
        return
    fileName = sys.argv[1]
    txtFileLocation = fileName + ".txt"
    annFileLocation = fileName + ".ann"
    # outputLocation = os.path.splitext(fileLocation)[0] + ".ann"
    with open(txtFileLocation, 'r') as txtFileHandler, open(annFileLocation, 'r+') as annFileHandler:
        start, end, token , startSorted, endSorted, tokenSorted = [], [], [], [], [], []
        for line in annFileHandler:
            print line
            m = re.search('(T\d+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(.+)', line) #token_id, token_name, start, end, token
            start.append(int(m.group(3)))
            end.append(int(m.group(4)))
            token.append(m.group(5))
        if start:
            startSorted, endSorted, tokenSorted = (list(x) for x in zip(*sorted(zip(start, end, token))))
        annFileHandler.seek(0)
        annFileHandler.truncate()

        processedLength = 0
        listLength = len(startSorted)
        tokenId = 1
        listIndex = 0
        tokenName = "Token"
        for line in txtFileHandler:
            if re.match("^Post-(\d)+.*Question-(\d)+$", line):
                processedLength += len(line)
                continue
            lineLength = len(line)
            lineIndex = 0
            while lineIndex < lineLength:
                if (listIndex < listLength):
                    if startSorted[listIndex] <= processedLength+lineIndex:
                        annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(startSorted[listIndex]) + " " + str(
                            endSorted[listIndex]) + "\t" + tokenSorted[listIndex] + "\n")
                        lineIndex = endSorted[listIndex] - processedLength
                        tokenId += 1
                        listIndex += 1
                    else:
                        nextNonwordIndex = -1
                        for i,n in enumerate(line[lineIndex:]):
                            if not n.isalnum():
                                nextNonwordIndex = i + lineIndex
                                break
                        if (nextNonwordIndex <= -1):
                            nextNonwordIndex = lineLength
                        if startSorted[listIndex] <= processedLength + nextNonwordIndex:
                            word=line[lineIndex:startSorted[listIndex]-processedLength]
                            annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(processedLength + lineIndex) + " " + str(
                                startSorted[listIndex]) + "\t" + word + "\n")
                            lineIndex = startSorted[listIndex] - processedLength
                            tokenId += 1
                        else:
                            if lineIndex == nextNonwordIndex: #word contains only whitespace or symbols
                                word = line[lineIndex:nextNonwordIndex+1]
                                if word.isspace():
                                    lineIndex += 1
                                else:
                                    annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(
                                        processedLength + lineIndex) + " " + str(
                                        processedLength + nextNonwordIndex + 1) + "\t" + word + "\n")
                                    lineIndex = nextNonwordIndex + 1
                                    tokenId += 1
                            else:
                                word = line[lineIndex:nextNonwordIndex]
                                annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(processedLength + lineIndex) + " " + str(
                                    processedLength + nextNonwordIndex) + "\t" + word + "\n")
                                lineIndex = nextNonwordIndex
                                tokenId += 1
                else:
                    nextNonwordIndex = -1
                    for i, n in enumerate(line[lineIndex:]):
                        if not n.isalnum():
                            nextNonwordIndex = i + lineIndex
                            break
                    if (nextNonwordIndex <= -1):
                        nextNonwordIndex = lineLength
                    if lineIndex == nextNonwordIndex:  # word contains only whitespace or symbols
                        word = line[lineIndex:nextNonwordIndex + 1]
                        if word.isspace():
                            lineIndex += 1
                        else:
                            annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(
                                processedLength + lineIndex) + " " + str(
                                processedLength + nextNonwordIndex + 1) + "\t" + word + "\n")
                            lineIndex = nextNonwordIndex + 1
                            tokenId += 1
                    else:
                        word = line[lineIndex:nextNonwordIndex]
                        annFileHandler.write("T" + str(tokenId) + "\t" + tokenName + " " + str(processedLength + lineIndex) + " " + str(
                            processedLength + nextNonwordIndex) + "\t" + word + "\n")
                        lineIndex = nextNonwordIndex
                        tokenId += 1
            processedLength += lineLength

if __name__ == '__main__':
    main()
