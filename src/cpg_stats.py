"""CpG depletion in a genome assembly.

For each sequence and for the whole assembly, reports the observed/expected
ratio of CpG dinucleotides, with GpC as a control:

    observed/expected = count(XY) * L / (count(X) * count(Y))

where L is the number of A, C, G and T bases. Values near 1 mean the
dinucleotide occurs as often as expected from base composition alone.
CpG depletion (values well below 1) is the long-term footprint of
methylated cytosines in CpG mutating to TpG in the germline.

Usage: python3 src/cpg_stats.py <assembly.fasta> [number_to_list]
"""
import sys

from fasta_utils import read_fasta

def dinucleotide_counts(seq):
    """Return counts needed for CpG and GpC observed/expected for one sequence."""
    upper = seq.upper()
    c = upper.count("C")
    g = upper.count("G")
    return {
        "c": c,
        "g": g,
        "acgt": c + g + upper.count("A") + upper.count("T"),
        "cg": upper.count("CG"),
        "gc": upper.count("GC"),
    }


def obs_exp(pair_count, x_count, y_count, length):
    """Observed/expected ratio of a dinucleotide (0 if it cannot be computed)."""
    expected = x_count * y_count / length if length > 0 else 0
    return pair_count / expected if expected > 0 else 0

if len(sys.argv) not in (2, 3):
    print("Usage: python3 src/cpg_stats.py <assembly.fasta> [number_to_list]",
          file=sys.stderr)
    sys.exit(1)

path = sys.argv[1]
number_to_list = int(sys.argv[2]) if len(sys.argv) == 3 else 30

# 1. Counts for every sequence (name, length, counts)
records = []
for name, seq in read_fasta(path):
    records.append((name, len(seq), dinucleotide_counts(seq)))
if not records:
    print(f"Error: no sequences found in {path}", file=sys.stderr)
    sys.exit(1)

# 2. Totals for the whole assembly
total = {key: sum(counts[key] for _, _, counts in records)
         for key in ("c", "g", "acgt", "cg", "gc")}
cpg_oe = obs_exp(total["cg"], total["c"], total["g"], total["acgt"])
gpc_oe = obs_exp(total["gc"], total["g"], total["c"], total["acgt"])

# 3. Report
print(f"File:               {path}")
print(f"Sequences:          {len(records)}")
print(f"A+C+G+T bases:      {total['acgt']:,}")
print(f"CpG count:          {total['cg']:,}")
print(f"GpC count:          {total['gc']:,}")
print(f"CpG obs/exp:        {cpg_oe:.3f}")
print(f"GpC obs/exp:        {gpc_oe:.3f}   (control)")

print("\nLargest sequences:")
print("rank\tname\tlength_bp\tCpG_count\tCpG_obs_exp\tGpC_obs_exp")
records.sort(key=lambda r: r[1], reverse=True)
for rank, (name, length, counts) in enumerate(records[:number_to_list], start=1):
    cpg = obs_exp(counts["cg"], counts["c"], counts["g"], counts["acgt"])
    gpc = obs_exp(counts["gc"], counts["g"], counts["c"], counts["acgt"])
    print(f"{rank}\t{name}\t{length}\t{counts['cg']}\t{cpg:.3f}\t{gpc:.3f}")

