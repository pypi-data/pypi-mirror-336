# Define the URL and the target file name
FILE="lips.xyz"
URL="https://archive.materialscloud.org/record/file?record_id=1302&filename=lips.xyz"

# Check if the file already exists
if [ -f "$FILE" ]; then
    echo "[INFO] File '$FILE' already exists. Skipping download."
else
    echo "[INFO] File '$FILE' not found."
    echo "[INFO] Downloading data. Please hold."
    # Download the file with wget, handling potential redirects
    wget --content-disposition "$URL"
fi

echo "[INFO] Splitting datasets into train/test/val with seed=42"
echo "[INFO] If you wish to split again differently use the split_data.py in the upper folder with a given rng seed"
python ../split_data.py lips.xyz --seed 42
