import numpy as np
import matplotlib.pyplot as plt

def main():
    questionQty = np.array([25,46,65,65,59,42,35,29,24,15,16,10,7,10,12,4,5,7,3,3,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1])
    ansLabels = np.char.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13','14', '15', '16', '17', '18', '19', '20', '22', '23', '24', '25','26', '27', '32', '33', '34', '37', '38', '39', '41', '71', '73','100'])

    percent = 100.*questionQty/questionQty.sum()

    labels = ['{0} - {1:1.2f} % '.format(ansLabel, percentage) for ansLabel, percentage in zip(ansLabels, percent)]

    patches, texts = plt.pie(questionQty, shadow=True, startangle=90)
    plt.legend(patches, labels, bbox_to_anchor=(0.1, 1.115), loc=1, fontsize=23, borderaxespad=1.0)
    fig = plt.gcf()
    fig.suptitle('Distribution of questions having X number of answers', fontsize=40)
    fig.set_size_inches(20,18)
    plt.savefig('piechart_distribution.png')
    plt.show()

if __name__ == "__main__":
    main()