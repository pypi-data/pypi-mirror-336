#!/bin/bash
set -eu

files=( "ML_AB_128h2o_validation.xyz" "ML_AB_dataset_1.xyz" "ML_AB_dataset_2.xyz" "ML_AB_dataset_2-val.xyz" )

all_exist=true
for file in "${files[@]}"; do
    if [ ! -e "$file" ]; then
        all_exist=false
    fi
done
if $all_exist; then
    echo "Files already exist, nothing to do."
    exit 0
fi

echo "Downloading files..."
wget -O data.zip https://zenodo.org/api/records/10723405/files-archive

echo "Extracting archive..."
unzip data.zip

echo "Converting files to XYZ format..."
python convert_vasp_mlff_to_xyz.py -f ML_AB_dataset_1
python convert_vasp_mlff_to_xyz.py -f ML_AB_dataset_2
python convert_vasp_mlff_to_xyz.py -f ML_AB_128h2o_validation

echo "Creating validation file..."
python remove_overlap.py

echo "Cleaning up..."
rm ML_AB_dataset_1 ML_AB_dataset_2 ML_AB_128h2o_validation data.zip
