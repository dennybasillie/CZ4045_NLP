export PATH_LIST=""
for i in {1..4}
do
    export PATH_LIST+=" ../annotated_dataset/Post-$i.ann"
    export PATH_LIST+=" ../tokenizer/Post-$i.ann"
done

python validator.py $PATH_LIST > validator-result.txt