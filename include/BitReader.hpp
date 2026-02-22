#ifndef BIT_READER_HPP
#define BIT_READER_HPP

#include <fstream>
#include <map>

class BitReader {
private:
    std::ifstream inFile;
    unsigned char buffer;
    int bitCount;

public:
    BitReader(const std::string& filename);
    ~BitReader();

    // Lê o cabeçalho e reconstrói o mapa de frequências
    std::map<char, unsigned> readHeader();

    // Retorna o próximo bit do arquivo (0 ou 1). Retorna -1 se chegar ao fim.
    int readBit();
    
    bool isOpen() const { return inFile.is_open(); }
    bool eof() const { return inFile.eof() && bitCount == 0; }
};

#endif