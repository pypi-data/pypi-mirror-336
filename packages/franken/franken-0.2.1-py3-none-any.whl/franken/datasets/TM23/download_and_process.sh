#!/bin/bash
set -eu

echo "Downloading files..."
wget --content-disposition "https://archive.materialscloud.org/record/file?record_id=2113&filename=benchmarking_master_collection-20240316T202423Z-001.zip"

echo "Extracting archive..."
unzip -j benchmarking_master_collection-20240316T202423Z-001.zip

read -p "Do you wish to keep all datasets including temperature-specific datasets(cold/warm/melt)? (yes/no): " answer

# Check if the answer is 'yes' (case-insensitive)
if [[ "$answer" == [Yy][Ee][Ss] || "$answer" == [Yy] ]]; then
    echo "Datasets ready."
else
    echo "Deleting temperature-specific datasets..."
    rm *cold*
    rm *warm*
    rm *melt*

fi

echo "Cleaning up..."
rm benchmarking_master_collection-20240316T202423Z-001.zip
