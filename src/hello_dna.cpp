#include <iostream>
#include <string>

int main() {
    std::string dna = "ACGTTACGGA";
    int gc = 0;

    for (char base : dna) {
        if (base == 'G' || base == 'C'){
            gc = gc + 1;
        }
    }
    
    std::cout << "Sequence " << dna << "\n";
    std::cout << "Length:  " << dna.size() << "\n";
    std::cout << "G+C:     " << gc << "\n";
    return 0;
}