"""Summary statistics for a genome assembly in FASTA format.

Reports the number of sequences, total length, N50/L50, gaps (runs of N),
soft-masked (lowercase) fraction and GC content, followed by a table of
the largest sequences.

Usage: python3 src/assembly_stats.py <assembly.fasta> [number_to_list]
"""
import re
import string
import sys


def read_fasta(path):
    """Yield (name, sequence) for each record in a FASTA file, one at a time."""
    name = None
    parts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(parts)
                name = line[1:].split()[0]
                parts = []
            else:
                parts.append(line)
    if name is not None:
        yield name, "".join(parts)


def sequence_stats(name, seq):
    """Return a dictionary of statistics for one sequence."""
    upper = seq.upper()
    gc = upper.count("G") + upper.count("C")
    return {
        "name": name,
        "length": len(seq),
        "gc": gc,
        "acgt": gc + upper.count("A") + upper.count("T"),
        "n_bases": upper.count("N"),
        "gaps": len(re.findall("N+", upper)),
        "masked": sum(seq.count(letter) for letter in string.ascii_lowercase),
    }


def n50_l50(lengths):
    """Return (N50, L50) for a list of sequence lengths."""
    total = sum(lengths)
    running = 0
    for count, length in enumerate(sorted(lengths, reverse=True), start=1):
        running += length
        if running >= total / 2:
            return length, count
    return 0, 0


def percent(part, whole):
    """Return part as a percentage of whole (0 if whole is 0)."""
    return 100 * part / whole if whole > 0 else 0


if len(sys.argv) not in (2, 3):
    print("Usage: python3 src/assembly_stats.py <assembly.fasta> [number_to_list]",
          file=sys.stderr)
    sys.exit(1)

path = sys.argv[1]
number_to_list = int(sys.argv[2]) if len(sys.argv) == 3 else 30

# 1. Statistics for every sequence
stats = [sequence_stats(name, seq) for name, seq in read_fasta(path)]
if not stats:
    print(f"Error: no sequences found in {path}", file=sys.stderr)
    sys.exit(1)

# 2. Totals for the whole assembly
lengths = [s["length"] for s in stats]
total_length = sum(lengths)
total_gc = sum(s["gc"] for s in stats)
total_acgt = sum(s["acgt"] for s in stats)
total_n = sum(s["n_bases"] for s in stats)
total_gaps = sum(s["gaps"] for s in stats)
total_masked = sum(s["masked"] for s in stats)
n50, l50 = n50_l50(lengths)

# 3. Sort sequences from longest to shortest
stats.sort(key=lambda s: s["length"], reverse=True)

# 4. Report
print(f"File:               {path}")
print(f"Sequences:          {len(stats)}")
print(f"Total length (bp):  {total_length:,}")
print(f"Longest (bp):       {stats[0]['length']:,}  ({stats[0]['name']})")
print(f"Shortest (bp):      {stats[-1]['length']:,}")
print(f"N50 (bp):           {n50:,}")
print(f"L50:                {l50}")
print(f"N bases:            {total_n:,}  ({percent(total_n, total_length):.2f} %)")
print(f"Gaps (runs of N):   {total_gaps:,}")
print(f"Soft-masked:        {percent(total_masked, total_length):.2f} %")
print(f"GC content:         {percent(total_gc, total_acgt):.2f} %")

print("\nLargest sequences:")
print("rank\tname\tlength_bp\tGC_percent\tN_bases\tgaps\tmasked_percent")
for rank, s in enumerate(stats[:number_to_list], start=1):
    print(f"{rank}\t{s['name']}\t{s['length']}\t"
          f"{percent(s['gc'], s['acgt']):.2f}\t{s['n_bases']}\t{s['gaps']}\t"
          f"{percent(s['masked'], s['length']):.2f}")