// assembly_stats.cpp
// Summary statistics for a genome assembly in FASTA format:
// number of sequences, total length, N50/L50, gaps (runs of N),
// soft-masked (lowercase) fraction and GC content,
// followed by a table of the largest sequences.
//
// Compile: g++ -std=c++17 -Wall -Wextra -O2 -o bin/assembly_stats src/assembly_stats.cpp
// Run:     ./bin/assembly_stats <assembly.fna> [number_of_sequences_to_list]

#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

// Statistics for one sequence (chromosome, scaffold or contig)
struct SeqStats {
    std::string name;
    long long length = 0;
    long long n_bases = 0;      // N or n
    long long lower = 0;        // soft-masked (lowercase) bases
    long long gc = 0;           // G or C, either case
    long long acgt = 0;         // A, C, G or T, either case
    long long gaps = 0;         // runs of consecutive N
};

// Update the statistics of one sequence with one line of bases.
// in_gap remembers whether the previous base was N, so that a gap
// spanning two lines is counted only once.
void add_line(SeqStats& s, const std::string& line, bool& in_gap) {
    for (char base : line) {
        s.length++;
        if (base >= 'a' && base <= 'z') {
            s.lower++;
        }
        switch (base) {
            case 'G': case 'g': case 'C': case 'c':
                s.gc++;
                s.acgt++;
                in_gap = false;
                break;
            case 'A': case 'a': case 'T': case 't':
                s.acgt++;
                in_gap = false;
                break;
            case 'N': case 'n':
                s.n_bases++;
                if (!in_gap) {
                    s.gaps++;
                }
                in_gap = true;
                break;
            default:
                in_gap = false;
                break;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0] << " <assembly.fasta> [number_of_sequences_to_list]\n";
        return 1;
    }
    std::size_t to_list = 30;
    if (argc == 3) {
        to_list = std::stoul(argv[2]);
    }

    std::ifstream file(argv[1]);
    if (!file) {
        std::cerr << "Error: cannot open file " << argv[1] << "\n";
        return 1;
    }

    // Read all sequences
    std::vector<SeqStats> seqs;
    std::string line;
    bool in_gap = false;
    while (std::getline(file, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();                       // Windows line endings
        }
        if (line.empty()) {
            continue;
        }
        if (line[0] == '>') {
            SeqStats s;
            // name = header text up to the first space
            s.name = line.substr(1, line.find(' ') - 1);
            seqs.push_back(s);
            in_gap = false;
        } else if (!seqs.empty()) {
            add_line(seqs.back(), line, in_gap);
        }
    }
    if (seqs.empty()) {
        std::cerr << "Error: no sequences found in " << argv[1] << "\n";
        return 1;
    }

    // Totals over the whole assembly
    SeqStats total;
    for (const SeqStats& s : seqs) {
        total.length += s.length;
        total.n_bases += s.n_bases;
        total.lower += s.lower;
        total.gc += s.gc;
        total.acgt += s.acgt;
        total.gaps += s.gaps;
    }

    // Sort from longest to shortest
    std::sort(seqs.begin(), seqs.end(),
              [](const SeqStats& x, const SeqStats& y) { return x.length > y.length; });

    // N50: length of the sequence at which the running total reaches half the assembly.
    // L50: how many sequences are needed to reach that point.
    long long running = 0;
    long long n50 = 0;
    std::size_t l50 = 0;
    for (std::size_t i = 0; i < seqs.size(); i++) {
        running += seqs[i].length;
        if (2 * running >= total.length) {
            n50 = seqs[i].length;
            l50 = i + 1;
            break;
        }
    }

    double gc_percent = total.acgt > 0 ? 100.0 * total.gc / total.acgt : 0.0;
    double masked_percent = 100.0 * total.lower / total.length;
    double n_percent = 100.0 * total.n_bases / total.length;

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "File:               " << argv[1] << "\n";
    std::cout << "Sequences:          " << seqs.size() << "\n";
    std::cout << "Total length (bp):  " << total.length << "\n";
    std::cout << "Longest (bp):       " << seqs.front().length << "  (" << seqs.front().name << ")\n";
    std::cout << "Shortest (bp):      " << seqs.back().length << "\n";
    std::cout << "N50 (bp):           " << n50 << "\n";
    std::cout << "L50:                " << l50 << "\n";
    std::cout << "N bases:            " << total.n_bases << "  (" << n_percent << " %)\n";
    std::cout << "Gaps (runs of N):   " << total.gaps << "\n";
    std::cout << "Soft-masked:        " << masked_percent << " %\n";
    std::cout << "GC content:         " << gc_percent << " %\n";

    std::cout << "\nLargest sequences:\n";
    std::cout << "rank\tname\tlength_bp\tGC_percent\tN_bases\tgaps\tmasked_percent\n";
    for (std::size_t i = 0; i < seqs.size() && i < to_list; i++) {
        const SeqStats& s = seqs[i];
        double s_gc = s.acgt > 0 ? 100.0 * s.gc / s.acgt : 0.0;
        double s_masked = 100.0 * s.lower / s.length;
        std::cout << i + 1 << "\t" << s.name << "\t" << s.length << "\t"
                  << s_gc << "\t" << s.n_bases << "\t" << s.gaps << "\t" << s_masked << "\n";
    }
    return 0;
}