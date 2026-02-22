#ifndef BIT_WRITER_HPP
#define BIT_WRITER_HPP

#include <fstream>
#include <string>

class BitWriter {
private:
    std::ofstream outFile;
    unsigned char buffer; // Buffer de 8 bits
    int bitCount;         // Contador de bits inseridos no buffer

public:
    BitWriter(const std::string& filename);
    ~BitWriter();

    void writeBit(int bit);
    void writeString(const std::string& bitString);
    void flush(); // Garante que bits restantes sejam escritos
};

#endif