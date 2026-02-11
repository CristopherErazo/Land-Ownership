#!/bin/bash

# Decompress and rename .gz files

DIRS=(
    "./data/farm_subsidy/2023"
    "./data/farm_subsidy/2024")

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Processing: $dir"
        cd "$dir"
        
        for file in *.gz; do
            if [ -f "$file" ]; then
                # Extract country code (first 2 characters)
                country="${file:0:2}"
                
                # Decompress
                gunzip "$file"
                
                # Rename to country code only
                mv "${file%.gz}" "$country.csv"
                echo "  $file → $country.csv"

                # Remove the original .gz file if it still exists
                if [ -f "$file" ]; then
                    rm "$file"
                fi
            fi
        done
        
        cd - > /dev/null
    fi
done

echo "Done!"