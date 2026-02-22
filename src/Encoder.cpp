#include "../include/Encoder.hpp"

void Encoder::encodeRecursive(Node* root, std::string code, std::map<char, std::string>& huffmanCode) {
    if (root == nullptr) return;

    // Se encontrar uma folha (caractere real), salva o código acumulado
    if (!root->left && !root->right) {
        huffmanCode[root->data] = code;
    }

    // Percorre para a esquerda (0) e direita (1)
    encodeRecursive(root->left, code + "0", huffmanCode);
    encodeRecursive(root->right, code + "1", huffmanCode);
}

std::map<char, std::string> Encoder::generateCodes(Node* root) {
    std::map<char, std::string> huffmanCode;
    encodeRecursive(root, "", huffmanCode);
    return huffmanCode;
}