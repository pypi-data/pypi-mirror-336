#!/bin/bash

for dir in */; do
  echo "Entering directory: $dir"
  cd "$dir"
  if [ -f "download_and_process.sh" ]; then
    echo "Executing download_and_process.sh..."
    bash download_and_process.sh
  fi
  cd ..
done