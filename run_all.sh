#!/bin/bash

# Define the Python files to run
files=(
    "src/data_collection.py"
    "src/preprocessing.py"
    "src/sentiment_analysis.py"
    "src/model.py"
    "src/evaluation.py"
)

# Loop through each file and run it
for file in "${files[@]}"; do
    echo "Running $file..."
    python3 "$file"
    if [ $? -eq 0 ]; then
        echo "$file executed successfully."
    else
        echo "Error executing $file."
        exit 1  # Exit if there is an error
    fi
done

echo "All scripts executed."
