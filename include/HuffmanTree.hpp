#ifndef HUFFMAN_TREE_HPP
#define HUFFMAN_TREE_HPP

#include <map>
#include <queue>
#include <vector>

struct Node {
    char data;
    unsigned freq;
    Node *left, *right;

    Node(char data, unsigned freq) : data(data), freq(freq), left(nullptr), right(nullptr) {}
};

// Comparador para a Priority Queue
struct Compare {
    bool operator()(Node* l, Node* r) {
        return (l->freq > r->freq);
    }
};

class HuffmanTree {
public:
    static Node* build(std::map<char, unsigned>& frequencies);
};

#endif