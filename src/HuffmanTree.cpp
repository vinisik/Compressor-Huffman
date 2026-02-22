#include "../include/HuffmanTree.hpp"

Node* HuffmanTree::build(std::map<char, unsigned>& frequencies) {
    std::priority_queue<Node*, std::vector<Node*>, Compare> minHeap;

    for (auto const& pair : frequencies) {
        char ch = pair.first;      
        unsigned freq = pair.second; 
        minHeap.push(new Node(ch, freq));
    }

    while (minHeap.size() > 1) { // Garante que saia quando restar apenas 1
        Node *left = minHeap.top();
        minHeap.pop();

        Node *right = minHeap.top();
        minHeap.pop();

        // Criando o nó pai com caractere nulo/especial
        Node *top = new Node('\0', left->freq + right->freq);
        top->left = left;
        top->right = right;

        minHeap.push(top);
    }

    return minHeap.empty() ? nullptr : minHeap.top();
}