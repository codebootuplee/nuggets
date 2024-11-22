#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <search_string>"
    exit 1
fi

DIRECTORY=$1
SEARCH_STRING=$2

# Check if the specified directory exists
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Directory $DIRECTORY does not exist."
    exit 1
fi

echo "Searching for '$SEARCH_STRING' in files under '$DIRECTORY'..."

# Use grep to search for the string in all files within the directory tree
MATCHES=$(grep -rnl "$DIRECTORY" -e "$SEARCH_STRING")

if [ -z "$MATCHES" ]; then
    echo "No matches found for '$SEARCH_STRING'."
else
    echo "Matches found:"
    echo "$MATCHES"
fi
