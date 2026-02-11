#!/bin/bash

# Script to download files from Google Drive folder

# Google Drive folder link (replace with your actual link)
GDRIVE_FOLDER_LINKS=(
    "https://drive.google.com/drive/u/2/folders/1igKTPLQxxrsC1DjQRmMdoQvNjcHeiaHc"
    "https://drive.google.com/drive/u/2/folders/1CyQIYFzi8GQy0Z8VABa77LsiqzOhKL2v")


# Output directory (relative to script location)
OUTPUT_DIRS=(
    "./data/farm_subsidy/2023"
    "./data/farm_subsidy/2024")

echo "========================================"
echo "Google Drive Folder Download Script"
echo "========================================"

# For each link download the data to the corresponding output directory
for i in "${!GDRIVE_FOLDER_LINKS[@]}"; do
    g_link="${GDRIVE_FOLDER_LINKS[$i]}"
    output_dir="${OUTPUT_DIRS[$i]}"
    echo "Downloading from: $g_link"
    echo "Saving to: $output_dir"
    mkdir -p "$output_dir"
    
    # For shared folders, don't exit on failure - just continue
    # The --remaining-ok flag helps with partial downloads
    gdown --folder "$g_link" -O "$output_dir" --remaining-ok --fuzzy || true
    
    echo ""
    echo "Download attempt completed for folder $((i+1))"
    echo "Check: $output_dir"
    echo ""
    
    # Add a small delay between folders to avoid rate limiting
    if [ $i -lt $((${#GDRIVE_FOLDER_LINKS[@]} - 1)) ]; then
        echo "Waiting 5 seconds before next folder..."
        sleep 5
    fi
done

echo "========================================"
echo "All download attempts completed!"
echo "Note: If some files failed, try running the script again."
echo "Already downloaded files will be skipped."
echo "========================================"