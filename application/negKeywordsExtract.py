import sys
from pycorenlp import StanfordCoreNLP

def main():

    nlp = StanfordCoreNLP('http://localhost:9000')

    negationWords = []

    with open(sys.argv[1], 'r') as f:
        for line in f:
            text = line.rstrip()
            output = nlp.annotate(text, properties={'annotators': 'depparse', 'outputFormat': 'json'})

            try:
                dep = output['sentences'][0]['basicDependencies']

                for i in range(len(dep)):
                    if dep[i]['dep'] == 'neg':
                        word = dep[i]['dependentGloss']
                        if word == "n't":
                            dep_temp = dep[i - 1]
                            if dep_temp['dep'] == 'expl':
                                word = dep_temp['governorGloss'] + word
                            else:
                                word = dep_temp['dependentGloss'] + word

                        word = word.lower()

                        if word not in negationWords:
                            negationWords.append(word)

        except:
            pass

if __name__ == "__main__":
    main()