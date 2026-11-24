# genome-tools

Python tools for vertebarate genome analysis, written from scratch.

This repository documents my work on building genome analysis tools, towards whole-genome comparative analyses of vertebrate assemblies.

## Tools

| Program | What it does | 
|---|---|
| `src/fasta_gc.py` | Reads a Fasta file; reports length, base composition
(A/C/G/T/N/other), GC content and GC skew |

## Requirements

Python 3 

## Usage 

    python src/fasta_gc.py <file.fasta>

Example:
    bash scripts/download_cod_mito.sh
    python3 src/fasta_gc.py data/raw/cod_mito.fasta

## Data
Genome data is not stored in this repoistory. Download scripts are in `scripts/`:

| Data | Source | Script |
|---|---|---|
| Atlantic cod (*Gadus morhua*) mitochondrial genome | NCBI NC_002081.1 |
`scripts/download_cod_mito.sh` |
| Atalantic cod reference genome assembly (gadMor3.0) | NCBI GCF_902167405.1 | `scripts/download_cod_genome.sh |

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

The downloaded cod genome assebmly was verified against NCBI's md5 checksum.

## Project structure
    src/ Python source code
    scripts/ data download scripts
    doc/ saved results
    data/raw/ downloaded genomes (not tracked by git)
    results/ program outputs (not tracked by git)