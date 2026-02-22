#include <iostream>
#include "include/HuffmanTree.hpp"
#include "include/FileHandler.hpp"
#include "include/Encoder.hpp"
#include "include/BitWriter.hpp"

int main() {
    std::string inputFile = "data/teste.txt";
    std::string outputFile = "data/teste.huff";

    auto freqs = FileHandler::getFrequencies(inputFile);
    Node* root = HuffmanTree::build(freqs);
    auto dictionary = Encoder::generateCodes(root);

    // Gravação dos bits
    BitWriter writer(outputFile);
    
    // Abre o original para ler e converter cada caractere em bits
    std::ifstream in(inputFile, std::ios::binary);
    char ch;
    while (in.get(ch)) {
        writer.writeString(dictionary[ch]);
    }
    
    std::cout << "Compressao concluida com sucesso!" << std::endl;
    return 0;
}