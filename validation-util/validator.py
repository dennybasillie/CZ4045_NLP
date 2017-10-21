##############
# Preprocessing
# Get rid of all spaces in all tokens, because it will mess up the validation method (using length)

false_positive = 0
false_negative = 0
start_char_GT = 0
start_char_model = 0
end_char_GT = None
end_char_model = None
length_GT = len(ground_truth)
length_model = len(model)
index_GT = 0
index_model = 0

# Traverse each token in both lists
while index_GT < length_GT and index_model < length_model:
   end_char_GT = start_char_GT + len(ground_truth[index_GT]) - 1
   end_char_model = start_char_model + len(ground_truth[index_model]) - 1
   if end_char_model == end_char_GT:
      index_GT += 1
      start_char_GT = end_char_GT + 1
      index_model += 1
      start_char_model = end_char_model + 1

   elif end_char_model < end_char_GT:
      index_model += 1
      start_char_model = end_char_model + 1
      false_positive += 1

   elif end_char_model > end_char_GT:
      index_GT += 1
      start_char_GT = end_char_GT + 1
      false_negative += 1

# See if thereis