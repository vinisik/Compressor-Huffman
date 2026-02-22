#include "../include/BitReader.hpp"

BitReader::BitReader(const std::string& filename) : buffer(0), bitCount(0) {
    inFile.open(filename, std::ios::binary);
}

BitReader::~BitReader() {
    if (inFile.is_open()) inFile.close();
}

std::map<char, unsigned> BitReader::readHeader() {
    std::map<char, unsigned> frequencies;
    size_t mapSize;
    
    // Lê o tamanho do mapa
    inFile.read(reinterpret_cast<char*>(&mapSize), sizeof(mapSize));

    // Lê cada par (caractere, frequência)
    for (size_t i = 0; i < mapSize; ++i) {
        char ch;
        unsigned freq;
        inFile.get(ch);
        inFile.read(reinterpret_cast<char*>(&freq), sizeof(freq));
        frequencies[ch] = freq;
    }
    return frequencies;
}

int BitReader::readBit() {
    if (bitCount == 0) {
        if (!inFile.get(reinterpret_cast<char&>(buffer))) return -1;
        bitCount = 8;
    }

    // Extrai o bit mais à esquerda 
    int bit = (buffer >> (bitCount - 1)) & 1;
    bitCount--;
    return bit;
}