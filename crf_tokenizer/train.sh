export CLASSPATH=$(find "../stanford-ner-java" -name '*.jar' | xargs echo | tr ' ' ':')
for i in {1..4}
do
    java edu.stanford.nlp.ie.crf.CRFClassifier -prop train-$i-prop.txt 2> train-$i-log.txt
done
