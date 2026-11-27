"""Shared helpers for reading FASTA files."""


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