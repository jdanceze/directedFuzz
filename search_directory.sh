#!/bin/bash

# Usage: ./search_directory.sh <directory> <string>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <directory> <string>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Error: $1 is not a directory"
    exit 1
fi

echo "Searching for '$2' in files inside '$1'..."
grep -r "$2" "$1"
