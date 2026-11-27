#!/bin/bash
# Run assembly_stats.py and cpg_stats.py on every genome in data/species.txt.
# Results are written to docs/<short_name>_assembly_stats.txt and
# docs/<short_name>_cpg_stats.txt.

mkdir -p docs
tail -n +2 data/species.txt | while read -r short_name accession assembly_name species || [ -n "$short_name" ]; do
    fasta=$(find "data/raw/$short_name" -name "*_genomic.fna" | head -n 1)
    if [ -z "$fasta" ]; then
        echo "Skipping $short_name: no genome file found in data/raw/$short_name" >&2
        continue
    fi
    echo "Analysing $short_name ($species)"
    python3 src/assembly_stats.py "$fasta" > "docs/${short_name}_assembly_stats.txt"
    python3 src/cpg_stats.py "$fasta" > "docs/${short_name}_cpg_stats.txt"
done
echo "Finished. Results are in docs/"