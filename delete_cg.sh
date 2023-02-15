#!/bin/bash

# The directory where the files are located
dir="/Users/jdanceze/Desktop/hub/tf_callgraph"

# The string to match
target_string="TEST"

# Loop through the files in the directory
for file in "$dir"/*; do
  
  # Get the first line of the file
  first_line=$(head -n 1 "$file")

  # Check if the first line matches the target string
  if [[ $first_line == *"$target_string"* ]]; then
    # If it does, delete the file
    echo "$file"
    rm "$file"
  fi
done
