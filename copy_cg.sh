#!/bin/bash
for file in `ls /Users/jdanceze/Downloads/callgraph_tf/tensorflow/html`
do
 if [[ $file == *_cgraph.dot ]]; then
  echo $file
  cp $file /Users/jdanceze/Desktop/hub/tf_callgraph
 fi
done