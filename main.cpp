#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "include/FileHandler.hpp"
#include "include/HuffmanTree.hpp"
#include "include/Encoder.hpp"
#include "include/BitWriter.hpp"
#include "include/BitReader.hpp"

// Função auxiliar para obter tamanho do arquivo
long long getFileSize(const std::string& filename) {
    std::ifstream in(filename, std::ifstream::ate | std::ifstream::binary);
    return in.tellg(); 
}

void compressFile(const std::string& inputPath, const std::string& outputPath, int level) {
    std::cout << "INFO:Analisando frequencias..." << std::endl;
    auto freqs = FileHandler::getFrequencies(inputPath);
    if (freqs.empty()) {
        std::cerr << "ERRO:Arquivo vazio ou invalido." << std::endl;
        return;
    }

    std::cout << "INFO:Construindo a Arvore de Huffman..." << std::endl;
    Node* root = HuffmanTree::build(freqs);
    auto dictionary = Encoder::generateCodes(root);

    BitWriter writer(outputPath);
    writer.writeHeader(freqs);

    std::ifstream in(inputPath, std::ios::binary);
    char ch;
    long long totalBytes = getFileSize(inputPath);
    long long processedBytes = 0;
    int lastPercent = -1;

    std::cout << "INFO:Comprimindo dados (Nivel " << level << ")..." << std::endl;
    
    // Pipeline de Compressão
    while (in.get(ch)) {
        writer.writeString(dictionary[ch]);
        processedBytes++;
        
        // Calcula a percentagem e emite apenas se mudar 
        int percent = (processedBytes * 100) / totalBytes;
        if (percent > lastPercent) {
            std::cout << "PROGRESS:" << percent << std::endl;
            lastPercent = percent;
        }
    }
    in.close();
    std::cout << "INFO:Concluido!" << std::endl;
}

void decompressFile(const std::string& inputPath, const std::string& outputPath) {
    std::cout << "INFO:Lendo cabecalho..." << std::endl;
    BitReader reader(inputPath);
    if (!reader.isOpen()) {
        std::cerr << "ERRO:Nao foi possivel abrir o arquivo comprimido." << std::endl;
        return;
    }

    auto freqs = reader.readHeader();
    Node* root = HuffmanTree::build(freqs);
    std::ofstream out(outputPath, std::ios::binary);
    Node* current = root;
    int bit;
    
    unsigned long long totalChars = 0;
    for (auto const& pair : freqs) totalChars += pair.second;
    unsigned long long charsProcessed = 0;
    int lastPercent = -1;

    std::cout << "INFO:Extraindo dados..." << std::endl;
    while (totalChars > 0 && (bit = reader.readBit()) != -1) {
        current = (bit == 0) ? current->left : current->right;
        
        if (!current->left && !current->right) {
            out.put(current->data);
            current = root;
            totalChars--;
            charsProcessed++;
            
            // Emite progresso na descompressão
            int percent = (charsProcessed * 100) / (charsProcessed + totalChars);
            if (percent > lastPercent) {
                std::cout << "PROGRESS:" << percent << std::endl;
                lastPercent = percent;
            }
        }
    }
    out.close();
    std::cout << "INFO:Concluido!" << std::endl;
}

int main(int argc, char* argv[]) {
    // ./huffman <modo> <input> <output> [nivel]
    if (argc < 4) {
        std::cerr << "Uso: " << argv[0] << " <-c|-d> <input> <output> [nivel]" << std::endl;
        return 1;
    }

    std::string option = argv[1];
    std::string input = argv[2];
    std::string output = argv[3];
    int level = (argc >= 5) ? std::stoi(argv[4]) : 1; // Nível padrão: 1

    if (option == "-c") compressFile(input, output, level);
    else if (option == "-d") decompressFile(input, output);
    else std::cerr << "ERRO:Opcao invalida!" << std::endl;

    return 0;
}