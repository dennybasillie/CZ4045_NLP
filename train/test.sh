export CLASSPATH=$(find "../stanford-ner-java" -name '*.jar' | xargs echo | tr ' ' ':')
for i in {1..4}
do
    java edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier tokenizer-$i.ser.gz -testFile test-$i.txt 1> output-$i.txt 2> score-$i.txt
done
