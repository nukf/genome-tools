# genome-tools

C++ tools for vertebrate genome analysis, written from scratch.

This repository documents my work on building genome analysis
tools step by step, towards whole-genome comparative analyses of vertebrate
assemblies (e.g. Vertebrate Genomes Project data).

## Tools

| Program | What it does |
|---|---|
| `fasta_gc` | Reads a FASTA file; reports length, base composition (A/C/G/T/N/other), GC content and GC skew |
| `assembly_stats` | Genome assembly statistics: number of sequences, total length, N50/L50, gaps (runs of N), soft-masked (repeat) fraction, GC content, and a table of the largest sequences |

## Build

    g++ -std=c++17 -Wall -Wextra -O2 -o bin/fasta_gc src/fasta_gc.cpp
    g++ -std=c++17 -Wall -Wextra -O2 -o bin/assembly_stats src/assembly_stats.cpp
## Usage

    ./bin/fasta_gc <file.fasta>
    ./bin/assembly_stats <assembly.fna> [number_of_sequences_to_list]

Example:

    bash scripts/download_cod_mito.sh
    ./bin/fasta_gc data/raw/cod_mito.fasta

## Data

Genome data is not stored in this repository. Download scripts are in `scripts/`:

| Data | Source | Script |
|---|---|---|
| Atlantic cod (*Gadus morhua*) mitochondrial genome | NCBI NC_002081.1 | `scripts/download_cod_mito.sh` |
| Atlantic cod (*Gadus morhua*) reference genome, gadMor3.0 | NCBI GCF_902167405.1 | `scripts/download_cod_genome.sh` |

The genome download was verified with the MD5 checksum supplied by NCBI.

## Results

### Atlantic cod reference genome (gadMor3.0)

`assembly_stats` reproduces the published assembly statistics:

| Measure | assembly_stats | Published |
|---|---|---|
| Sequences | 227 | 226 scaffolds + mitochondrial genome |
| Total length | 669,966,409 bp | 669,949,713 bp (Ensembl) + 16,696 bp mitogenome |
| N50 | 28,732,775 bp | 28,732,775 bp (Ensembl scaffold N50) |
| L50 | 11 | |
| Chromosomes | 23 largest sequences = 23 chromosomes (21.7–43.8 Mb) | 23 chromosomes |
| Gaps (runs of N) | 1,216 | ~1,215 (1,441 contigs in 226 scaffolds) |
| N bases | 3.52% | |
| Soft-masked (repeats) | 31.74% | |
| GC content | 45.64% | |

Run time: about 5 s on a laptop (Apple M-series) for the full 670 Mb assembly.

Unplaced scaffolds are much more repeat-rich (often 50–80% soft-masked)
than the chromosomes (28–35%), consistent with repeats being the main
obstacle to placing sequences during assembly.

Full output: [docs/cod_gadMor3_assembly_stats.txt](docs/cod_gadMor3_assembly_stats.txt)

### Atlantic cod mitochondrial genome (NC_002081.1):

| Measure | Value | Checked against |
|---|---|---|
| File size | 16,993 bytes | curl download report; `wc -c` |
| Length | 16,696 bp | NCBI record length; `grep`/`tr`/`wc` count |
| A / C / G / T | 4,684 / 4,273 / 2,798 / 4,941 | sum = 16,696 |
| N / other | 0 / 0 | |
| GC content | 42.35% | |
| GC skew (G−C)/(G+C) | −0.209 | hand calculation: (2798−4273)/(2798+4273) |

The strong C/G imbalance (C > G, GC skew −0.21) is a known strand-composition
asymmetry of vertebrate mitochondrial genomes, thought to reflect mutation
(e.g. cytosine deamination) on the strand left single-stranded during
mitochondrial DNA replication.

## Project structure

    src/        C++ source code
    scripts/    data download scripts
    data/raw/   downloaded genomes (not tracked by git)
    data/test/  small test files
    bin/        compiled programs (not tracked by git)
    results/    program outputs (not tracked by git)