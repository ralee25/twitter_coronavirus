#!/bin/bash

# Directory where the tweet files are located
INPUT_DIR="/data/Twitter dataset"
OUTPUT_DIR="./output"

mkdir -p "$OUTPUT_DIR"

# Loop over all the 2020 tweet zip files
for file in "$INPUT_DIR"/geoTwitter20-*.zip; do
    # Extract the output folder name based on the input file name
    filename=$(basename "$file")
    
    # Run map.py on each file in parallel using nohup
    echo "Processing $filename..."
    nohup python3 map.py "$file" "$OUTPUT_DIR" > "$filename" 2>&1 &

done

echo "All map.py processes have been started in parallel."
