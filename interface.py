import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compressor")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        self.label = tk.Label(self.main_frame, text="Compressor Huffman", font=("Segoe UI", 16, "bold"))
        self.label.pack(pady=(0, 20))

        # Botões
        style = {"width": 35, "font": ("Segoe UI", 10), "cursor": "hand2"}

        self.btn_compress = tk.Button(self.main_frame, text="Comprimir Arquivo (-c)", 
                                      command=self.compress_action, bg="#e1f5fe", **style)
        self.btn_compress.pack(pady=10)

        self.btn_decompress = tk.Button(self.main_frame, text="Descompactar Arquivo (-d)", 
                                        command=self.decompress_action, bg="#f3e5f5", **style)
        self.btn_decompress.pack(pady=10)

        # Status
        self.status_var = tk.StringVar(value="Status: Aguardando seleção...")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var, 
                                     font=("Segoe UI", 9, "italic"), fg="gray")
        self.status_label.pack(side="bottom", pady=10)

    def get_size_format(self, b):
        """Formata bytes para um formato legível (KB, MB, etc)"""
        for unit in ["B", "KB", "MB", "GB"]:
            if b < 1024:
                return f"{b:.2f} {unit}"
            b /= 1024

    def run_command(self, option, input_path, output_path):
        # Detecta se é Windows para usar .exe
        executable = "./bin/huffman.exe" if os.name == 'nt' else "./bin/huffman"
        
        if not os.path.exists(executable):
            messagebox.showerror("Erro", "Executável não encontrado!\nCertifique-se de rodar 'make' no terminal antes.")
            return False

        try:
            self.status_var.set("Status: Processando... por favor aguarde.")
            self.root.update_idletasks()
            
            result = subprocess.run([executable, option, input_path, output_path], 
                                    capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                messagebox.showerror("Erro no C++", f"Ocorreu um erro na lógica interna:\n{result.stderr}")
                return False
        except Exception as e:
            messagebox.showerror("Erro de Sistema", f"Falha ao executar o comando:\n{str(e)}")
            return False
        finally:
            self.status_var.set("Status: Pronto")

    def compress_action(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo para comprimir")
        if not file_path:
            return

        output_path = file_path + ".huff"
        if self.run_command("-c", file_path, output_path):
            self.show_report(file_path, output_path, "Compressão")

    def decompress_action(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo .huff", 
                                               filetypes=[("Huffman Files", "*.huff")])
        if not file_path:
            return

        output_path = file_path.replace(".huff", "_recovered.txt")
        if self.run_command("-d", file_path, output_path):
            messagebox.showinfo("Sucesso", f"Arquivo descompactado com sucesso!\nSalvo como: {os.path.basename(output_path)}")

    def show_report(self, original, compressed, tipo):
        size_in = os.path.getsize(original)
        size_out = os.path.getsize(compressed)
        
        # Cálculo da porcentagem de economia
        ratio = (1 - (size_out / size_in)) * 100
        
        report = (
            f"Relatório de {tipo}\n"
            f"{'-'*30}\n"
            f"Input: {os.path.basename(original)} ({self.get_size_format(size_in)})\n"
            f"Output: {os.path.basename(compressed)} ({self.get_size_format(size_out)})\n"
            f"{'-'*30}\n"
            f"Economia de Espaço: {ratio:.2f}%"
        )
        
        if ratio < 0:
            report += "\n\nNota: O arquivo aumentou devido ao cabeçalho (comum em arquivos pequenos)."
            messagebox.showwarning("Resultado", report)
        else:
            messagebox.showinfo("Resultado", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()