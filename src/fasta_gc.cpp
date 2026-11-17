// fasta_gc.cpp
// Read one DNA sequence from a FASTA file and report its length,
// base composition and GC content.
//
// Compile: g++ -std=c++17 -Wall -Wextra -O2 -o bin/fasta_gc src/fasta_gc.cpp
// Run:     ./bin/fasta_gc data/raw/cod_mito.fasta

#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    // 1. Check the user gave exactly one file name
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <file.fasta>\n";
        return 1;
    }

    // 2. Open the file
    std::ifstream file(argv[1]);
    if (!file) {
        std::cerr << "Error: cannot open file " << argv[1] << "\n";
        return 1;
    }

    // 3. Read the file line by line
    std::string header;
    std::string sequence;
    std::string line;
    while (std::getline(file, line)) {
        if (line.empty()) {
            continue;                 // skip blank lines
        }
        if (line[0] == '>') {
            header = line;            // the description line
        } else {
            sequence += line;         // sequence lines together
        }
    }

    // 4. Count each kind of base
    long a = 0, c = 0, g = 0, t = 0, n = 0, other = 0;
    for (char base : sequence) {
        if (base == 'A' || base == 'a') {
            a++;
        } else if (base == 'C' || base == 'c') {
            c++;
        } else if (base == 'G' || base == 'g') {
            g++;
        } else if (base == 'T' || base == 't') {
            t++;
        } else if (base == 'N' || base == 'n') {
            n++;
        } else {
            other++;
        }
    }

    // 5. Calculate GC content (ignoring N and other letters)
    long acgt = a + c + g + t;
    double gc_percent = 0.0;
    if (acgt > 0) {
        gc_percent = 100.0 * (g + c) / acgt;
    }

    // 6. Print the report
    std::cout << "Header: " << header << "\n";
    std::cout << "Length: " << sequence.size() << "\n";
    std::cout << "A: " << a << "  C: " << c << "  G: " << g
              << "  T: " << t << "  N: " << n << "  other: " << other << "\n";
    std::cout << "GC content: " << gc_percent << " %\n";
    
    // 7. GC skew
    double gc_skew = 0.0;
    if (g + c > 0) {
        gc_skew = static_cast<double>(g - c) / (g + c);
    }
    std::cout << "GC skew: " << gc_skew << "\n";

    return 0;
}