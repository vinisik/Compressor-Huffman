#ifndef FILE_HANDLER_HPP
#define FILE_HANDLER_HPP

#include <string>
#include <map>

class FileHandler {
public:
    static std::map<char, unsigned> getFrequencies(const std::string& filename);
};

#endif