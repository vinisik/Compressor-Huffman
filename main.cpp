#include <iostream>
#include "include/HuffmanTree.hpp"
#include "include/FileHandler.hpp"
#include "include/Encoder.hpp"

int main() {
    std::string path = "data/teste.txt";
    
    auto freqs = FileHandler::getFrequencies(path);
    if (freqs.empty()) return 1;

    Node* root = HuffmanTree::build(freqs);

    // Gerar o dicionário de códigos
    std::map<char, std::string> dictionary = Encoder::generateCodes(root);

    std::cout << "--- Dicionario de Huffman ---" << std::endl;
    for (auto const& pair : dictionary) {
        std::cout << "'" << pair.first << "': " << pair.second << std::endl;
    }

    return 0;
}