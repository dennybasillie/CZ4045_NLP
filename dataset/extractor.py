import sys
from lxml import etree

def main():
    # the file to be extracted from
    posts = sys.argv[1]
    questionsFile = sys.argv[2]
    answersFile = sys.argv[3]

    # initialise variables for querying xml element tree
    limit = 500
    n = 0
    questionIds = []
    questionDict = {}
    lang = "<java>"
    attTags = "Tags"
    attAnsCount = "AnswerCount"

    # parse element tree iteratively for 'questions' first, as the xml file is too large for memory
    context = etree.iterparse(posts)

    for action, element in context:
        if (n == limit):
            break
        if (attTags in element.attrib and lang in element.attrib[attTags] and int(element.attrib[attAnsCount]) > 0):
            questionIds.append(element.attrib["Id"])
            questionDict[element.attrib["Id"]] = element.attrib["Body"]
            n = n + 1
            element.clear()

    print(len(questionIds))

    # re-parse element tree for 'answers', because previous iterations not in memory anymore
    context = etree.iterparse(posts)

    for action, element in context:
        if (attAns in element.attrib and element.attrib[attAns] in questionIds):
            answer = {"answerId": element.attrib["Id"], "questionId": element.attrib[attAns], "answer": element.attrib["Body"]}
            with open(answersFile, "a") as f:
                try:
                    f.write(str(answer) + "\n")
                except:
                    continue
        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]

    for questionId in questionIds:
        question = {"questionId": questionId, "question": questionDict[questionId]}
        with open(questionsFile, "a") as f:
            try:
                f.write(str(question) + "\n")
            except:
                continue

    questionCount = countPosts(questionsFile)
    answerCount = countPosts(answersFile)

    print("Extraction complete! Total question count: %d, total answer count: %d"%(questionCount, answerCount))

def countPosts(file):
    count = 0

    with open(file, "r") as f:
        while (True):
            line = f.readline()
            if line == "":
                break
            count += 1

    return count

if __name__ == "__main__":
    main()