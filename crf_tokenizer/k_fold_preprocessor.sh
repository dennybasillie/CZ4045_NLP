export PATH_LIST=""
for i in {1..4}
do
    export PATH_LIST+=" ../annotated_dataset/Post-$i.conll"
done

python k_fold_preprocessor.py $PATH_LIST