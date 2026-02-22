#ifndef ENCODER_HPP
#define ENCODER_HPP

#include "HuffmanTree.hpp"
#include <map>
#include <string>

class Encoder {
public:
    // Gera o mapa de códigos percorrendo a árvore
    static std::map<char, std::string> generateCodes(Node* root);

private:
    // Função auxiliar recursiva
    static void encodeRecursive(Node* root, std::string code, std::map<char, std::string>& huffmanCode);
};

#endif