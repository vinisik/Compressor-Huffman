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
    std::cout << "Lendo frequencias..." << std::endl;
    auto freqs = FileHandler::getFrequencies(inputPath);
    if (freqs.empty()) return;

    std::cout << "Construindo arvore e dicionario..." << std::endl;
    Node* root = HuffmanTree::build(freqs);
    auto dictionary = Encoder::generateCodes(root);

    BitWriter writer(outputPath);
    writer.writeHeader(freqs);

    std::ifstream in(inputPath, std::ios::binary);
    char ch;
    std::cout << "Comprimindo bits..." << std::endl;
    while (in.get(ch)) {
        writer.writeString(dictionary[ch]);
    }
    in.close();
    std::cout << "Arquivo comprimido com sucesso: " << outputPath << std::endl;
}

// Função para descompactar um arquivo
void decompressFile(const std::string& inputPath, const std::string& outputPath) {
    BitReader reader(inputPath);
    if (!reader.isOpen()) {
        std::cerr << "Erro ao abrir arquivo comprimido." << std::endl;
        return;
    }

    std::cout << "Lendo cabecalho..." << std::endl;
    auto freqs = reader.readHeader();
    
    std::cout << "Reconstruindo arvore..." << std::endl;
    Node* root = HuffmanTree::build(freqs);

    std::ofstream out(outputPath, std::ios::binary);
    Node* current = root;
    int bit;

    // Calcula o total de caracteres para evitar o padding do ultimo byte
    unsigned long long totalChars = 0;
    for (auto const& pair : freqs) {
        totalChars += pair.second;
    }

    std::cout << "Extraindo dados..." << std::endl;
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
    std::cout << "Arquivo descompactado com sucesso: " << outputPath << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cout << "Uso: " << argv[0] << " <opcao> <entrada> <saida>" << std::endl;
        std::cout << "Opcoes:\n  -c : Comprimir\n  -d : Descompactar" << std::endl;
        return 1;
    }

    std::string option = argv[1];
    std::string input = argv[2];
    std::string output = argv[3];

    if (option == "-c") {
        compressFile(input, output);
    } else if (option == "-d") {
        decompressFile(input, output);
    } else {
        std::cerr << "Opcao invalida!" << std::endl;
        return 1;
    }

    return 0;
}