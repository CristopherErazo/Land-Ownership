#!/bin/bash

# Decompress and rename .gz files

DIRS=(
    "./data_raw/farm_subsidy/2016"
    "./data_raw/farm_subsidy/2017")

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

        # For csv files just change the name
        for file in *.csv; do
            if [ -f "$file" ]; then
                # Extract country code (first 2 characters)
                country="${file:0:2}"
                
                # Rename to country code only
                mv "$file" "$country.csv"
                echo "  $file → $country.csv"
            fi
        done
        
        cd - > /dev/null
    fi
done

echo "Done!"