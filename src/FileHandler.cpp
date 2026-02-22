#include "../include/FileHandler.hpp"
#include <fstream>
#include <iostream>

std::map<char, unsigned> FileHandler::getFrequencies(const std::string& filename) {
    std::map<char, unsigned> freqMap;
    std::ifstream file(filename, std::ios::binary);

    if (!file.is_open()) {
        return freqMap;
    }

    char ch;
    while (file.get(ch)) {
        freqMap[ch]++;
    }

    file.close();
    return freqMap;
}