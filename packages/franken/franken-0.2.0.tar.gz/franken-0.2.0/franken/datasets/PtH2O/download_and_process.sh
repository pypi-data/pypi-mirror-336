#!/bin/bash
set -eu

url="https://data.dtu.dk/ndownloader/files/29141586"
files=( "train.extxyz" "valid.extxyz" "test.extxyz" )

all_exist=true
for file in "${files[@]}"; do
    if [ ! -e "$file" ]; then
        echo $file " does not exist"
        all_exist=false
    fi
done
if $all_exist; then
    echo "Files already exist, nothing to do."
    exit 0
fi

echo "Downloading files..."
wget -O data.zip $url

echo "Extracting archive..."
# unzips a directory called 'Dataset_and_training_files'. We want file 'dataset.traj' within it
unzip data.zip

echo "Splitting dataset into train/test/val..."
cd Dataset_and_training_files
python ../split.py
mv *extxyz dataset.traj ../

echo "Cleaning up..."
cd ..
rm -r Dataset_and_training_files data.zip