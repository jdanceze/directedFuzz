#!/bin/bash
for file in `ls /Users/jdanceze/Desktop/hub/tf_callgraph`
do
 if [[ $file == *_cgraph.dot ]]; then
  echo $file
  sed -i '' 's/\\l//' $file
 fi
done