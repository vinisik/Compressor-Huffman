#include <iostream>
#include <string>
#include <vector>
#include "include/FileHandler.hpp"
#include "include/HuffmanTree.hpp"
#include "include/Encoder.hpp"
#include "include/BitWriter.hpp"
#include "include/BitReader.hpp"

// Função para comprimir um arquivo
void compressFile(const std::string& inputPath, const std::string& outputPath) {
    auto freqs = FileHandler::getFrequencies(inputPath);
    if (freqs.empty()) return;
    Node* root = HuffmanTree::build(freqs);
    auto dictionary = Encoder::generateCodes(root);
    BitWriter writer(outputPath);
    writer.writeHeader(freqs);
    std::ifstream in(inputPath, std::ios::binary);
    char ch;
    while (in.get(ch)) {
        writer.writeString(dictionary[ch]);
    }
    in.close();
}

// Função para descompactar um arquivo
void decompressFile(const std::string& inputPath, const std::string& outputPath) {
    BitReader reader(inputPath);
    if (!reader.isOpen()) return;
    auto freqs = reader.readHeader();
    Node* root = HuffmanTree::build(freqs);
    std::ofstream out(outputPath, std::ios::binary);
    Node* current = root;
    int bit;

    // Calcula o total de caracteres para evitar o padding do ultimo byte
    unsigned long long totalChars = 0;
    for (auto const& pair : freqs) totalChars += pair.second;
    while (totalChars > 0 && (bit = reader.readBit()) != -1) {
        if (bit == 0) current = current->left;
        else current = current->right;
        if (!current->left && !current->right) {
            out.put(current->data);
            current = root;
            totalChars--;
        }
    }
    out.close();
}

// Função para exibir apenas o dicionário 
void showInfo(const std::string& inputPath) {
    auto freqs = FileHandler::getFrequencies(inputPath);
    if (freqs.empty()) return;
    Node* root = HuffmanTree::build(freqs);
    auto dictionary = Encoder::generateCodes(root);
    std::cout << "---START_DICT---" << std::endl;
    for (auto const& pair : dictionary) {
        std::cout << (int)(unsigned char)pair.first << ":" << pair.second << std::endl;
    }
    std::cout << "---END_DICT---" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 3) return 1;
    std::string option = argv[1];
    if (option == "-i" && argc >= 3) {
        showInfo(argv[2]);
        return 0;
    }
    if (argc < 4) return 1;
    if (option == "-c") compressFile(argv[2], argv[3]);
    else if (option == "-d") decompressFile(argv[2], argv[3]);
    return 0;
}