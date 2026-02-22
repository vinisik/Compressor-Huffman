# Variáveis do Compilador
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Iinclude

# Diretórios
SRC_DIR = src
INC_DIR = include
OBJ_DIR = build
BIN_DIR = bin

# Arquivos
SOURCES = $(wildcard $(SRC_DIR)/*.cpp) main.cpp
OBJECTS = $(patsubst %.cpp, $(OBJ_DIR)/%.o, $(notdir $(SOURCES)))
TARGET = $(BIN_DIR)/huffman

# Regra principal 
all: setup $(TARGET)

# Cria as pastas necessárias
setup:
	@if not exist $(OBJ_DIR) mkdir $(OBJ_DIR)
	@if not exist $(BIN_DIR) mkdir $(BIN_DIR)

# Linkagem do executável final
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compilação dos arquivos de objeto (.o) a partir dos .cpp da pasta src
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Compilação do main.cpp
$(OBJ_DIR)/main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpeza dos arquivos gerados
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Atalho para rodar um teste rápido 
test: all
	./$(TARGET) -c data/teste.txt data/teste.huff
	./$(TARGET) -d data/teste.huff data/resultado.txt