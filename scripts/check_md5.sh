#!/bin/bash
# Verify the files of an NCBI datasets package against its md5sum.txt.
# Usage: bash scripts/check_md5.sh data/raw/<short_name>

folder="$1"
if [ ! -f "$folder/md5sum.txt" ]; then
    echo "Usage: bash scripts/check_md5.sh <folder containing md5sum.txt>" >&2
    exit 1
fi

failed=0
while read -r expected file; do
    if command -v md5 > /dev/null; then
        actual=$(md5 -q "$folder/$file")              # macOS
    else
        actual=$(md5sum "$folder/$file" | cut -d " " -f 1)   # Linux
    fi
    if [ "$actual" = "$expected" ]; then
        echo "OK    $file"
    else
        echo "BAD   $file"
        failed=1
    fi
done < "$folder/md5sum.txt"

if [ "$failed" -eq 0 ]; then
    echo "All files match NCBI's checksums."
else
    echo "Some files do not match: download again." >&2
    exit 1
fi