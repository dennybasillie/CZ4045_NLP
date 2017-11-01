import sys


def cal_precision(true_positive, false_positive):
    return float(true_positive) / (true_positive + false_positive)


def cal_recall(true_positive, false_negative):
    return float(true_positive) / (true_positive + false_negative)


def cal_f1_score(precision, recall):
    if precision == 0 or recall == 0:
        return 0
    return 2.0 * (precision * recall) / (precision + recall)


def main():
    if len(sys.argv) <= 1 or (len(sys.argv) - 1) % 2 == 1:
        print("Need at least an ann file as ground truth of a post and an ann file as tokenization result of a post")
        return
    
    arg_len = len(sys.argv)

    list_ground_truth_path = []
    list_model_path = []
    print(sys.argv)
    for i in range(1, arg_len, 2):
        list_ground_truth_path.append(sys.argv[i])
        list_model_path.append(sys.argv[i+1])
    
    len_post = len(list_model_path)
    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0

    total_length_GT = 0
    total_length_model = 0

    for i in range(len_post):
        ground_truth = []
        model = []
        ground_truth_path = list_ground_truth_path[i]
        model_path = list_model_path[i]

        with open(ground_truth_path, 'r') as ground_truth_file, open(model_path, 'r') as model_file:
            #some ground truth ann file are not sorted based on token number
            sorted_ground_truth_lines =  sorted(ground_truth_file.readlines(), key=lambda x: int(x.split()[0][1:]))
            sorted_model_lines = sorted(model_file.readlines(), key=lambda x: int(x.split()[0][1:]))

            for line in sorted_ground_truth_lines:
                split_res = line.split()
                token = ' '.join(split_res[4:])
                ground_truth.append(token)
            for line in sorted_model_lines:
                split_res = line.split()
                token = ' '.join(split_res[4:])
                model.append(token)

        # # Test data
        # ground_truth = ['good', 'day', 'to', 'you']
        # model = ['goo', 'dday', 't', 'o', 'you']

        false_positive = 0
        false_negative = 0
        start_char_GT = 0
        start_char_model = 0
        length_GT = len(ground_truth)
        length_model = len(model)
        index_GT = 0
        index_model = 0

        seen = [False] * length_model

        # Traverse each token in both lists
        while index_GT < length_GT and index_model < length_model:
            # Get rid of all spaces in all tokens, because it will mess up the validation method (using length)
            cur_token_GT = ground_truth[index_GT].replace(' ', '')
            cur_token_model = model[index_model].replace(' ', '')

            end_char_GT = start_char_GT + len(cur_token_GT) - 1
            end_char_model = start_char_model + len(cur_token_model) - 1

            # To prevent indexing error while looking at 'seen' list
            # when we have incremented index_model in the current iteration
            model_moved = False

            # Decide comparison progress
            if end_char_model < end_char_GT:
                index_model += 1
                start_char_model = end_char_model + 1
                model_moved = True
            elif end_char_model == end_char_GT:
                index_model += 1
                start_char_model = end_char_model + 1
                model_moved = True
                index_GT += 1
                start_char_GT = end_char_GT + 1
            elif end_char_model > end_char_GT:
                index_GT += 1
                start_char_GT = end_char_GT + 1
            else:
                print("Cannot decide how to progress.")

            # Prevent seen tokens to be considered in the scoring again
            if seen[index_model - model_moved]:
                continue

            # Decide whether it's correct / false positive / false negative
            if start_char_model < start_char_model or end_char_model > end_char_GT:
                false_negative += 1
            elif start_char_model > start_char_model or end_char_model < end_char_GT:
                false_positive += 1
            # Both have same start and end index, but confirm the tokens are equal, because whitespaces are removed
            elif cur_token_model != cur_token_GT:
                false_negative += 1

            seen[index_model - model_moved] = True
            model_moved = False

        # See if there is still additional tokens in any lists
        if index_GT < length_GT:
            false_negative += (length_GT - index_GT)
        elif index_model < length_model:
            false_positive += (length_model - index_model)

        true_positive = length_model - (false_positive + false_negative)

        # Calculate precision, recall, and F1 score
        precision = cal_precision(true_positive, false_positive)
        recall = cal_recall(true_positive, false_negative)
        f1_score = cal_f1_score(precision, recall)

        print("------ Model performance on Post %d-------" % (i+1))
        print("Total ground truth tokens: %d" % length_GT)
        print("Total model tokens: %d" % length_model)
        print("--------------------------------")
        print("True positive: %d (%.2f%%)" % (true_positive, float(true_positive) / length_model * 100))
        print("False positive: %d (%.2f%%)" % (false_positive, float(false_positive) / length_model * 100))
        print("False negative: %d (%.2f%%)" % (false_negative, float(false_negative) / length_model * 100))
        print("--------------------------------")
        print("Precision: %.3f" % precision)
        print("Recall: %.3f" % recall)
        print("F1 score: %.3f" % f1_score)
        print("--------------------------------")
        print
        #calculate all total
        total_true_positive += true_positive
        total_false_positive += false_positive
        total_false_negative += false_negative
        total_length_GT += length_GT
        total_length_model += length_model
    
    overall_precision = cal_precision(total_true_positive, total_false_positive)
    overall_recall = cal_recall(total_true_positive, total_false_negative)
    overall_f1_score = cal_f1_score(overall_precision, overall_recall)
    print("------ Overall model performance %d-------")
    print("Total ground truth tokens: %d" % total_length_GT)
    print("Total model tokens: %d" % total_length_model)
    print("--------------------------------")
    print("True positive: %d (%.2f%%)" % (total_true_positive, float(total_true_positive) / total_length_model * 100))
    print("False positive: %d (%.2f%%)" % (total_false_positive, float(total_false_positive) / total_length_model * 100))
    print("False negative: %d (%.2f%%)" % (total_false_negative, float(total_false_negative) / total_length_model * 100))
    print("--------------------------------")
    print("Precision: %.3f" % overall_precision)
    print("Recall: %.3f" % overall_recall)
    print("F1 score: %.3f" % overall_f1_score)
    print("--------------------------------")

if __name__ == "__main__":
    main()