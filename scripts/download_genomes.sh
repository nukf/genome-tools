#!/bin/bash
# Download every genome assembly listed in data/species.txt from NCBI.
# Each genome is unzipped into data/raw/<short_name>/ and the zip is removed.
# Genomes already present are skipped, so the script can simply be run again
# to retry any download that failed.
# Requires: NCBI datasets CLI (conda install -c conda-forge ncbi-datasets-cli)

mkdir -p data/raw
tail -n +2 data/species.txt | while read -r short_name accession assembly_name species || [ -n "$short_name" ]; do
    zip_file="data/raw/$short_name.zip"
    if [ -d "data/raw/$short_name" ]; then
        echo "Skipping $short_name: data/raw/$short_name already exists"
        continue
    fi
    echo "Downloading $short_name ($species, $assembly_name, $accession)"
    if ! datasets download genome accession "$accession" \
            --include genome --filename "$zip_file" < /dev/null; then
        echo "FAILED: download of $short_name. Run the script again to retry." >&2
        rm -f "$zip_file"
        continue
    fi
    if ! unzip -q -o "$zip_file" -d "data/raw/$short_name"; then
        echo "FAILED: unzip of $short_name. Run the script again to retry." >&2
        rm -rf "$zip_file" "data/raw/$short_name"
        continue
    fi
    rm "$zip_file"
    echo "Done: $short_name"
done