#ifndef BIT_WRITER_HPP
#define BIT_WRITER_HPP

#include <fstream>
#include <string>
#include <map>

class BitWriter {
private:
    std::ofstream outFile;
    unsigned char buffer; // Buffer de 8 bits
    int bitCount;         // Contador de bits inseridos no buffer

public:
    BitWriter(const std::string& filename);
    ~BitWriter();

    // Grava o cabeçalho com a tabela de frequências
    void writeHeader(const std::map<char, unsigned>& frequencies);
    // Grava um único bit (0 ou 1)
    void writeBit(int bit);
    // Grava uma string de bits
    void writeString(const std::string& bitString);
    // Garante que bits restantes sejam escritos
    void flush(); 
};

#endif