export CLASSPATH=$(find "../stanford-ner-java" -name '*.jar' | xargs echo | tr ' ' ':')
for i in {0..3}
do
    java edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier tokenizer-$i.ser.gz -testFile test-$i.txt 1> result-$i.txt 2> score-$i.txt
done
