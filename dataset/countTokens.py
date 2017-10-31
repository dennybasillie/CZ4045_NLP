import sys
from nltk.tokenize import WordPunctTokenizer

def main():
    """Uses WordPunctTokenizer. Returns the total number of tokens across all files passed as arguments. To run: python countTokens.py file1.txt file2.txt"""
    tokenCount = 0
    tokenizer = WordPunctTokenizer()
    argsLen = len(sys.argv) - 1

    for i in range(1, argsLen + 1):
        with open(sys.argv[i], 'r') as f:
            text = f.read()
        tokens = tokenizer.tokenize(text)
        tokenCount += len(tokens)
    print('Total token count: %d'%tokenCount)

if __name__ == "__main__":
    main()