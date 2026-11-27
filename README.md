# genome-tools

Python tools for vertebrate genome analysis, written from scratch.

This repository documents my work on building genome analysis tools, towards whole-genome comparative analyses of vertebrate assemblies.

## Tools

| Program | What it does | 
|---|---|
| `src/fasta_gc.py` | Reads a FASTA file; reports length, base composition (A/C/G/T/N/other), GC content and GC skew |
| `src/assembly_stats.py` | Genome assembly statistics: number of sequences, total length, N50/L50, gaps (runs of N), soft-masked (repeat) fraction, GC content, and a table of the largest sequences |

## Requirements

Python 3 

## Usage 
 
    python3 src/fasta_gc.py <file.fasta>
    python3 src/assembly_stats.py <assembly.fasta> [number_to_list]

Example:

    bash scripts/download_cod_mito.sh
    python3 src/fasta_gc.py data/raw/cod_mito.fasta

## Data
Genome data is not stored in this repository. Download scripts are in `scripts/`:

| Data | Source | Script |
|---|---|---|
| Atlantic cod (*Gadus morhua*) mitochondrial genome | NCBI NC_002081.1 |`scripts/download_cod_mito.sh` |
| Atlantic cod reference genome assembly (gadMor3.0) | NCBI GCF_902167405.1 | `scripts/download_cod_genome.sh` |

## Results

Atlantic cod mitochondrial genome (NC_002081.1):

| Measure | Value | Checked against |
|---|---|---|
| File size | 16,993 bytes | curl download report; `wc -c` |
| Length | 16,696 bp | NCBI record length; `grep`/`tr`/`wc` count |
| A / C / G / T | 4,684 / 4,273 / 2,798 / 4,941 | sum = 16,696 |
| N / other | 0 / 0 | |
| GC content | 42.35% | |
| GC skew (G−C)/(G+C) | −0.209 |

The strong C/G imbalance (C > G, GC skew -0.21) is a known strand-composition asymmetry of vertebrate mitochondrial genomes, thought to reflect mutation (e.g. cystosine deamination) on the strand left single-stranded during mitochondrial DNA replication.

The downloaded cod genome assembly was verified against NCBI's md5 checksum.

Atlantic cod reference genome assembly (gadMor3.0, GCF_902167405.1),
full output in `docs/cod_gadMor3_assembly_stats.txt`:

| Measure | Value | Checked against |
|---|---|---|
| Sequences | 227 (23 chromosomes, 203 unplaced scaffolds, 1 mitochondrial genome) | published: 226 scaffolds + mitochondrial genome |
| Total length | 669,966,409 bp | published 669,949,713 bp + 16,696 bp mitochondrial genome |
| Longest sequence | 43,798,135 bp (NC_044051.1) | |
| N50 / L50 | 28,732,775 bp / 11 | published scaffold N50 28,732,775 bp |
| N bases | 23,573,743 (3.52%) | |
| Gaps (runs of N) | 1,216 | published 1,441–1,442 contigs in 226 scaffolds |
| Soft-masked (repeat) fraction | 31.74% | |
| GC content | 45.64% | |
| Run time | 14 s (Python 3, MacBook Air) | |

## Project structure
    src/ Python source code
    scripts/ data download scripts
    docs/ saved results
    data/raw/ downloaded genomes (not tracked by git)
    results/ program outputs (not tracked by git)