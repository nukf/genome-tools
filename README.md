# genome-tools

C++ tools for vertebrate genome analysis, written from scratch.

This repository documents my work on building genome analysis
tools step by step, towards whole-genome comparative analyses of vertebrate
assemblies (e.g. Vertebrate Genomes Project data).

## Tools

| Program | What it does |
|---|---|
| `fasta_gc` | Reads a FASTA file; reports length, base composition (A/C/G/T/N/other), GC content and GC skew |

## Build

    g++ -std=c++17 -Wall -Wextra -O2 -o bin/fasta_gc src/fasta_gc.cpp

## Usage

    ./bin/fasta_gc <file.fasta>

Example:

    bash scripts/download_cod_mito.sh
    ./bin/fasta_gc data/raw/cod_mito.fasta

## Data

Genome data is not stored in this repository. Download scripts are in `scripts/`:

| Data | Source | Script |
|---|---|---|
| Atlantic cod (*Gadus morhua*) mitochondrial genome | NCBI NC_002081.1 | `scripts/download_cod_mito.sh` |

## Results

Atlantic cod mitochondrial genome (NC_002081.1):

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