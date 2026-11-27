"""Combine the per-species results in docs/ into one comparison table.

Reads data/species.txt and, for each species, the summary lines of
docs/<short_name>_assembly_stats.txt and docs/<short_name>_cpg_stats.txt.
Writes a tab-separated table to docs/species_summary.tsv and prints it.

Usage: python3 src/summarize_results.py
"""
import sys

FIELDS = {
    "Sequences:": "sequences",
    "Total length (bp):": "total_length_bp",
    "N50 (bp):": "n50_bp",
    "L50:": "l50",
    "Gaps (runs of N):": "gaps",
    "Soft-masked:": "masked_percent",
    "GC content:": "gc_percent",
    "CpG obs/exp:": "cpg_obs_exp",
    "GpC obs/exp:": "gpc_obs_exp",
}
COLUMNS = ["species", "assembly", "sequences", "total_length_bp", "n50_bp",
           "l50", "gaps", "masked_percent", "gc_percent", "cpg_obs_exp",
           "gpc_obs_exp"]


def read_summary(path):
    """Return {column: value} from the summary lines of one results file."""
    values = {}
    with open(path) as f:
        for line in f:
            for label, column in FIELDS.items():
                if line.startswith(label):
                    value = line[len(label):].split()[0]
                    values[column] = value.replace(",", "")
    return values


rows = []
with open("data/species.txt") as f:
    next(f)                                    # skip the header line
    for line in f:
        parts = line.split()
        if not parts:
            continue
        short_name, accession, assembly_name = parts[:3]
        species = " ".join(parts[3:])
        row = {"species": species, "assembly": assembly_name}
        try:
            row.update(read_summary(f"docs/{short_name}_assembly_stats.txt"))
            row.update(read_summary(f"docs/{short_name}_cpg_stats.txt"))
        except FileNotFoundError as error:
            print(f"Skipping {short_name}: {error}", file=sys.stderr)
            continue
        rows.append(row)

with open("docs/species_summary.tsv", "w") as out:
    out.write("\t".join(COLUMNS) + "\n")
    for row in rows:
        out.write("\t".join(row.get(column, "") for column in COLUMNS) + "\n")

with open("docs/species_summary.tsv") as f:
    print(f.read(), end="")