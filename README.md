# genome-tools

Python tools for vertebrate genome analysis, written from scratch.

This repository documents my work on building genome analysis tools, towards whole-genome comparative analyses of vertebrate assemblies.

## Tools

| Program | What it does | 
|---|---|
| `src/fasta_gc.py` | Reads a FASTA file; reports length, base composition (A/C/G/T/N/other), GC content and GC skew |
| `src/assembly_stats.py` | Genome assembly statistics: number of sequences, total length, N50/L50, gaps (runs of N), soft-masked (repeat) fraction, GC content, and a table of the largest sequences |
| `src/cpg_stats.py` | CpG depletion: observed/expected CpG for each sequence and the whole assembly, with GpC as a control |
| `src/fasta_utils.py` | Shared FASTA reader used by the tools |
| `src/summarize_results.py` | Combines per-species results into one comparison table (`docs/species_summary.tsv`) |
| `scripts/download_genomes.sh` | Downloads every genome listed in `data/species.txt`; safe to re-run to retry failed downloads |
| `scripts/check_md5.sh` | Verifies a downloaded genome against NCBI's md5 checksums |
| `scripts/run_all.sh` | Runs the analysis tools on every genome |

## Requirements

Python 3 

## Usage 
 
    python3 src/fasta_gc.py <file.fasta>
    python3 src/assembly_stats.py <assembly.fasta> [number_to_list]
    python3 src/cpg_stats.py <assembly.fasta> [number_to_list]

Example:

    bash scripts/download_cod_mito.sh
    python3 src/fasta_gc.py data/raw/cod_mito.fasta

Full multi-species workflow:

    bash scripts/download_genomes.sh
    bash scripts/check_md5.sh data/raw/<short_name>
    bash scripts/run_all.sh
    python3 src/summarize_results.py

## Data
Genome data is not stored in this repository. Download scripts are in `scripts/`:

| Data | Source | Script |
|---|---|---|
| Atlantic cod (*Gadus morhua*) mitochondrial genome | NCBI NC_002081.1 |`scripts/download_cod_mito.sh` |
| Atlantic cod reference genome assembly (gadMor3.0) | NCBI GCF_902167405.1 | `scripts/download_cod_genome.sh` |
| Five vertebrate reference genomes (list in `data/species.txt`) | NCBI | `scripts/download_genomes.sh` |

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


CpG depletion in gadMor3.0, full output in `docs/cod_gadMor3_cpg_stats.txt`:

| Measure | Value |
|---|---|
| CpG observed/expected | 0.592 |
| GpC observed/expected (control) | 0.904 |
| Range across the 23 chromosomes (CpG o/e) | 0.56–0.62 |

CpG dinucleotides occur at about 59% of the frequency expected from base
composition, while the reverse dinucleotide GpC is close to expectation.
This CpG-specific depletion is the expected long-term footprint of
methylated cytosines mutating to thymine in the germline. The value is
typical of fish genomes (about 0.5) and much higher than in mammals
(about 0.2), consistent with lower CpG depletion in fish.

### Comparison across five vertebrates

Five reference genome assemblies (`data/species.txt`), downloaded with
`scripts/download_genomes.sh`, verified with `scripts/check_md5.sh`,
analysed with `scripts/run_all.sh` and combined with
`src/summarize_results.py` (full table: `docs/species_summary.tsv`).

| Species | Group | Assembly | Sequences | Size (Gb) | N50 (Mb) | Gaps | Repeats (%) | GC (%) | CpG o/e | GpC o/e |
|---|---|---|---|---|---|---|---|---|---|---|
| Atlantic cod (*Gadus morhua*) | fish | gadMor3.0 | 227 | 0.67 | 28.7 | 1,216 | 31.7 | 45.6 | 0.592 | 0.904 |
| Zebrafish (*Danio rerio*) | fish | GRCz13ab | 26 | 1.46 | 59.4 | 0 | 51.8 | 37.2 | 0.501 | 1.157 |
| Zebra finch (*Taeniopygia guttata*) | bird | bTaeGut7.mat | 41 | 1.14 | 72.1 | 9 | 22.4 | 42.7 | 0.227 | 1.077 |
| Green sea turtle (*Chelonia mydas*) | reptile | rCheMyd1.pri.v2 | 93 | 2.13 | 134.4 | 298 | 31.4 | 44.0 | 0.261 | 1.009 |
| Human (*Homo sapiens*) | mammal | GRCh38.p14 | 705 | 3.30 | 145.1 | 1,169 | 36.1 | 41.1 | 0.243 | 1.015 |

CpG observed/expected agrees with published values for human (about 0.2)
and zebrafish (about 0.5). CpG depletion is clearly weaker in the two fish
(0.50–0.59) than in the bird, reptile and mammal (0.23–0.26), while the
GpC control stays close to 1 in all species.

Notes: totals include all sequences in each NCBI package, i.e. the
mitochondrial genome where present and, for human, alternative loci and
patch scaffolds (hence 705 sequences and 3.30 Gb rather than the 3.10 Gb
primary assembly).

## Project structure
    src/ Python source code
    scripts/    data download scripts
    docs/       saved results
    data/raw/   downloaded genomes (not tracked by git)
    results/    program outputs (not tracked by git)
    data/       species list (data/species.txt)