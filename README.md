# **Compressor de Arquivos com Codificação de Huffman**

Compressor de arquivos de alta performance baseado na **Codificação de Huffman**, uma técnica de compressão *lossless* que utiliza a frequência de caracteres para otimizar o armazenamento. O motor de processamento foi desenvolvido em **C++**, e a interface foi construída em **Python**.

## **Funcionalidades**

* **Compressão Lossless**: Redução do tamanho de arquivos sem perder um único bit de informação.  
* **Processamento Assíncrono (Multithread)**: A interface gráfica (GUI) não para durante operações longas, utilizando threads para acompanhar o progresso em tempo real.  
* **Processamento em Lote (Batch)**: Compressão automatizada de múltiplos arquivos de um diretório de uma só vez 
* **Pré-visualização de Dicionário**: Tabela interativa que mostra como a árvore de Huffman remapeou os códigos ASCII em bits.
* **Gerador de Testes Integrado**: Ferramenta na própria interface para criar arquivos `.txt` massivos com redundância, ideal para testar o stress e a taxa de compressão do algoritmo.
* **Relatórios e Histórico (Logs)**: Acompanhamento detalhado do tempo de execução, tamanhos e economia de espaço em %. 
* **Cabeçalho Binário**: Gravação inteligente da tabela de frequências no próprio arquivo `.huff` para permitir descompressão autônoma.  

## **Estrutura do Projeto**

* `bin/`: Contém o executável final (huffman.exe).  
* `build/`: Armazena os arquivos de objeto (.o) gerados na compilação.  
* `include/`: Definições das classes e cabeçalhos C++ (.hpp).  
* `src/`: Implementação da lógica do compressor (.cpp).  
* `gui\_compressor.py`: Interface gráfica para o usuário final.  
* `Makefile`: Automatização do processo de construção do projeto.
* `teste_arquivo.py`: Algoritmo que gera um arquivo .txt grande (500kb) com caracteres aleatórios para testar a compressão e descompressão
* `interface.py`:  Interface gráfica avançada com abas, progresso em tempo real e relatórios. 


## **Explicação dos Módulos**
### **1\. HuffmanTree (A Estrutura de Dados)**
O coração do algoritmo. Foi utilizada uma Fila de Prioridade (`std::priority_queue`) para construir a árvore de baixo para cima.
- Os caracteres com as menores frequências são unidos em nós pais até que reste apenas um único nó raiz.
- Resultado: Caracteres mais frequentes ficam mais perto da raiz (códigos menores), e os menos frequentes ficam mais longe (códigos maiores).

### **2\. Encoder (Gerando o Dicionário)**
Este módulo realiza uma travessia recursiva na árvore (DFS).
- Ao caminhar para a esquerda, atribui o bit `0`.
- Ao caminhar para a direita, atribui o bit `1`.
- Gera um mapa (`std::map<char, string>`) que permite a tradução instantânea de caracteres para suas novas representações binárias.

### **3\. BitWriter e BitReader (Manipulação de Baixo Nível)**
Como o computador só escreve bytes inteiros (8 bits), estes módulos lidam com a complexidade de "empacotar" bits individuais.
- BitWriter: Utiliza operadores de deslocamento (`<<`) e máscaras (`|`) para acumular bits em um buffer de 1 byte. Quando o buffer enche, ele é "despejado" no disco.
- BitReader: Realiza o inverso, lendo um byte e extraindo bit a bit para navegar na árvore de Huffman durante a descompressão.

### **4\. Comunicação C++/Python**
A integração entre Python e C++ é feita via stdout (saída padrão
- O motor C++ calcula o total de bytes e emite avisos de progresso regulares (ex: `PROGRESS:50`).
- O Python, rodando em uma thread separada via `subprocess.Popen`, lê essas linhas instantaneamente e atualiza as barras de progresso do Tkinter.


## **Como Utilizar**

### **1\. Compilação**

Para compilar o núcleo em C++, utilizar o terminal na raiz do projeto:

```
make
```
_Nota: Se o Windows não possuir o .exe make no bin do MinGW, usar `mingw32-make` ou duplicar o .exe do `mingw32-make` e renomear para `make`._

### **2\. Execução via Interface Gráfica**

Para utilizar o compressor com a janela visual:

```
python interface.py
```

### **3\. Execução via Linha de Comando (CLI)**

Também é possível utilizar o binário diretamente via terminal:

### Para Comprimir
```  
./bin/huffman \-c caminho/original.txt caminho/comprimido.huff
```

### Para Descompressão
```  
./bin/huffman \-d caminho/comprimido.huff caminho/resultado.txt
```


Este algoritmo é eficaz em arquivos de texto (`.txt`, `.csv`), arquivos de log e código-fonte. Em arquivos com alta redundância de caracteres, a taxa de compressão pode chegar a **40-60%** de economia.


Projeto desenvolvido por Vinicius Siqueira como estudo de algoritmos de compressão, estruturas de dados de baixo nível (C++) e integração inter-processos com interfaces Python. Parte da lógica base foi inspirada em conceitos de Algoritmos e Estrutura de Dados II.