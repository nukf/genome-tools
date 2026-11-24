""" Report length, base composition, GC content and GC skew of a FASTA file."""
import sys

def read_fasta(path):
    header = ""
    parts = []
    with open(path) as f:
        for line in f:
            line =line.strip() #space and \n
            if not line:
                continue
            if line.startswith(">"):
                header = line
            else:
                parts.append(line)
    return header, "".join(parts)

if len(sys.argv) != 2: 
    print ("Usage: python3 src/fasta_gc.py <file.fasta>", file = sys.stderr)
    sys.exit(1)

header, seq = read_fasta(sys.argv[1])
seq=seq.upper()

a = seq.count("A")
c = seq.count("C")
g = seq.count("G")
t = seq.count ("T")
n = seq.count ("N")
other = len(seq) - (a+c+g+t+n)

acgt = a+c+t+g
gc_percent = 100 * (g+c)/acgt if acgt > 0 else 0
gc_skew = (g-c)/(g+c) if (g+c) > 0 else 0

print("header:", header)
print("length:", len(seq))
print(f"A: {a} C: {c} G: {g} T: {t} N: {n} other: {other}")
print(f" Gc content: {gc_percent:.2f} %" )
print(f"GC skew: {gc_skew:.4f}")
