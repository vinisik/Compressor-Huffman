#include "../include/BitWriter.hpp"

BitWriter::BitWriter(const std::string& filename) : buffer(0), bitCount(0) {
    outFile.open(filename, std::ios::binary);
}

BitWriter::~BitWriter() {
    if (outFile.is_open()) {
        flush();
        outFile.close();
    }
}

void BitWriter::writeHeader(const std::map<char, unsigned>& frequencies) {
    if (!outFile.is_open()) return;

    // Escreve a quantidade de entradas no mapa
    size_t mapSize = frequencies.size();
    outFile.write(reinterpret_cast<const char*>(&mapSize), sizeof(mapSize));

    // Escreve cada par (caractere, frequência)
    for (auto const& pair : frequencies) {
        char ch = pair.first;
        unsigned freq = pair.second;
        outFile.put(ch);
        outFile.write(reinterpret_cast<const char*>(&freq), sizeof(freq));
    }
}

void BitWriter::writeBit(int bit) {
    // Desloca o buffer para a esquerda e adiciona o bit no final
    buffer <<= 1;
    if (bit) buffer |= 1;
    bitCount++;

    // Se completar 8 bits, escreve o byte no arquivo
    if (bitCount == 8) {
        outFile.put(buffer);
        buffer = 0;
        bitCount = 0;
    }
}

void BitWriter::writeString(const std::string& bitString) {
    for (char c : bitString) {
        writeBit(c == '1' ? 1 : 0);
    }
}

void BitWriter::flush() {
    // Se sobrar bits no buffer, empurra-os até completar o byte e grava
    if (bitCount > 0) {
        buffer <<= (8 - bitCount);
        outFile.put(buffer);
        bitCount = 0;
    }
}