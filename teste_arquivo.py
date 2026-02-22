import random
import string

def gerar_arquivo_grande(nome_arquivo, tamanho_kb):
    """Gera um arquivo de texto grande para fazer um teste de compressão que seja de melhor visualização"""
    caracteres = string.ascii_lowercase + " "
    pesos = [10 if c in 'aeiou ' else 1 for c in caracteres]
    
    conteudo = random.choices(caracteres, weights=pesos, k=tamanho_kb * 1024)
    
    with open(nome_arquivo, 'w') as f:
        f.write("".join(conteudo))
    
    print(f"Arquivo '{nome_arquivo}' gerado com {tamanho_kb} KB.")

if __name__ == "__main__":
    # Gera um arquivo de 500 KB 
    gerar_arquivo_grande("data/arquivo_teste.txt", 500)