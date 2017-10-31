import sys
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import WordPunctTokenizer

def main():
    tokenizer = WordPunctTokenizer()

    posts = []

    # 'questions-textonly.txt'
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line[:-1]
            posts.append(line)

    # 'answers-textonly.txt'
    with open(sys.argv[2], 'r') as f:
        for line in f:
            line = line[:-1]
            posts.append(line)

    #print(len(posts))

    posts_lengths = []

    for post in posts:
        tokens = tokenizer.tokenize(post)
        tokenCount = len(tokens)
        posts_lengths.append(tokenCount)

    #print(len(posts_lengths))

    posts_lengths.sort()

    posts_lengths_unique = set(posts_lengths)

    #print(len(posts_lengths_unique))

    posts_lengths_unique_list = list(posts_lengths_unique)

    posts_lengths_count = []

    prevCount = posts_lengths[0]
    currCount = posts_lengths[0]
    n = 0

    for i in range(len(posts_lengths)):
        currCount = posts_lengths[i]
        if (currCount == prevCount):
            n += 1
        else:
            posts_lengths_count.append(n)
            n = 1
        prevCount = currCount

    posts_lengths_count.append(n)

    #print(len(posts_lengths_count))

    #posts_lengths_unique_list.index(21)
    #posts_lengths_unique_list.index(101)
    #posts_lengths_unique_list.index(502)

    posts_lengths_counts = np.array(posts_lengths_count)
    posts_lengths_Counts = np.array([])
    posts_lengths_Counts = np.append(posts_lengths_Counts, posts_lengths_counts[0])
    posts_lengths_Counts = np.append(posts_lengths_Counts, posts_lengths_counts[1:21].sum())
    posts_lengths_Counts = np.append(posts_lengths_Counts, posts_lengths_counts[21:101].sum())
    posts_lengths_Counts = np.append(posts_lengths_Counts, posts_lengths_counts[101:387].sum())
    posts_lengths_Counts = np.append(posts_lengths_Counts, posts_lengths_counts[387:].sum())

    posts_labels = np.char.array(['0', '1~20', '21~100', '101~500', '>500'])
    percents = 100.*posts_lengths_Counts/posts_lengths_Counts.sum()
    labels = ['{0} - {1:1.2f} % '.format(label, percentage) for label, percentage in zip(posts_labels, percents)]

    patches, texts = plt.pie(posts_lengths_Counts, shadow=True, startangle=90)
    plt.legend(patches, labels, bbox_to_anchor=(0.2, 0.27), loc=1, fontsize='medium', borderaxespad=1.0)
    plt.title('Distribution of posts having X number of tokens')
    plt.savefig('posts_distribution.png')
    plt.show()

if __name__ == "__main__":
    main()