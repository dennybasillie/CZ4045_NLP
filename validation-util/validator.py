def cal_precision(true_positive, false_positive):
    return float(true_positive) / (true_positive + false_positive)


def cal_recall(true_positive, false_negative):
    return float(true_positive) / (true_positive + false_negative)


def cal_f1_score(precision, recall):
    if precision == 0 or recall == 0:
        return 0
    return 2.0 * (precision * recall) / (precision + recall)


def main():
    # Test data
    ground_truth = ['good', 'day', 'to', 'you']
    model = ['goo', 'dday', 't', 'o', 'you']

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

    print("------ Model performance -------")
    print("Total ground truth tokens: %d" % length_GT)
    print("Total model tokens: %d" % length_model)
    print("--------------------------------")
    print("True positive: %d (%.2f)" % (true_positive, float(true_positive) / length_model))
    print("False positive: %d (%.2f)" % (false_positive, float(false_positive) / length_model))
    print("False negative: %d (%.2f)" % (false_negative, float(false_negative) / length_model))
    print("--------------------------------")
    print("Precision: %.3f" % precision)
    print("Recall: %.3f" % recall)
    print("F1 score: %.3f" % f1_score)
    print("--------------------------------")


if __name__ == "__main__":
    main()