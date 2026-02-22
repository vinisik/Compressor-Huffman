#include <iostream>
#include "include/HuffmanTree.hpp"
#include "include/FileHandler.hpp"

int main() {
    std::string path = "data/teste.txt";
    
    // 1. Contagem
    auto freqs = FileHandler::getFrequencies(path);
    if (freqs.empty()) {
        std::cerr << "Ficheiro vazio ou nao encontrado!" << std::endl;
        return 1;
    }

    // 2. Construção da Árvore
    Node* root = HuffmanTree::build(freqs);

    std::cout << "Arvore de Huffman construida com sucesso!" << std::endl;
    std::cout << "Raiz (Frequencia Total): " << root->freq << std::endl;

    return 0;
}