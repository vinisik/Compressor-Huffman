import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import time
from datetime import datetime

class ModernHuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compressão Huffman - Interface")
        self.root.geometry("700x550")
        
        # Cores e Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_main = ttk.Frame(self.notebook)
        self.tab_batch = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_main, text=" Único Arquivo ")
        self.notebook.add(self.tab_batch, text=" Processamento em Lote ")
        self.notebook.add(self.tab_history, text=" Histórico/Logs ")
        
        self.setup_main_tab()
        self.setup_batch_tab()
        self.setup_history_tab()
        
        # Status Bar
        self.status_var = tk.StringVar(value="Pronto")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_main_tab(self):
        frame = ttk.Frame(self.tab_main, padding="20")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Selecione um arquivo para operar:", font=("Arial", 10, "bold")).pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Comprimir (.txt -> .huff)", command=self.compress_single).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Descompactar (.huff -> .txt)", command=self.decompress_single).grid(row=0, column=1, padx=5)
        
        # Tabela de Códigos
        ttk.Label(frame, text="Tabela de Códigos Huffman:").pack(pady=(20, 5), anchor="w")
        self.tree = ttk.Treeview(frame, columns=("Char", "ASCII", "Código"), show="headings", height=8)
        self.tree.heading("Char", text="Caractere")
        self.tree.heading("ASCII", text="Código ASCII")
        self.tree.heading("Código", text="Bits Huffman")
        self.tree.pack(expand=True, fill="both")

    def setup_batch_tab(self):
        frame = ttk.Frame(self.tab_batch, padding="20")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Comprimir todos os arquivos de uma pasta", font=("Arial", 10, "bold")).pack(pady=10)
        ttk.Button(frame, text="Selecionar Pasta", command=self.batch_process).pack(pady=5)
        
        self.batch_progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.batch_progress.pack(pady=20)
        
        self.batch_label = ttk.Label(frame, text="Aguardando comando...")
        self.batch_label.pack()

    def setup_history_tab(self):
        frame = ttk.Frame(self.tab_history, padding="10")
        frame.pack(expand=True, fill="both")
        
        self.log_text = tk.Text(frame, state='disabled', height=20, font=("Consolas", 9))
        self.log_text.pack(expand=True, fill="both")
        
        ttk.Button(frame, text="Limpar Histórico", command=self.clear_logs).pack(pady=5)

    def log(self, message):
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def get_bin(self):
        return "./bin/huffman.exe" if os.name == 'nt' else "./bin/huffman"

    def update_dict_preview(self, file_path):
        self.tree.delete(*self.tree.get_children())
        try:
            res = subprocess.run([self.get_bin(), "-i", file_path], capture_output=True, text=True)
            if "---START_DICT---" in res.stdout:
                lines = res.stdout.splitlines()
                start = False
                for line in lines:
                    if "---START_DICT---" in line: start = True; continue
                    if "---END_DICT---" in line: break
                    if start and ":" in line:
                        ascii_val, code = line.split(":", 1)
                        char_repr = chr(int(ascii_val))
                        if int(ascii_val) == 10: char_repr = "\\n"
                        elif int(ascii_val) == 32: char_repr = "(espaço)"
                        self.tree.insert("", tk.END, values=(char_repr, ascii_val, code))
        except Exception as e:
            self.log(f"Erro ao gerar preview: {e}")

    def compress_single(self):
        file_path = filedialog.askopenfilename()
        if not file_path: return
        
        self.update_dict_preview(file_path)
        out_path = file_path + ".huff"
        
        start_t = time.time()
        res = subprocess.run([self.get_bin(), "-c", file_path, out_path])
        end_t = time.time()
        
        if res.returncode == 0:
            size_in = os.path.getsize(file_path)
            size_out = os.path.getsize(out_path)
            ratio = (1 - size_out/size_in)*100
            msg = f"Sucesso: {os.path.basename(file_path)} comprimido ({ratio:.1f}% de economia) em {end_t-start_t:.3f}s"
            self.log(msg)
            messagebox.showinfo("Concluído", msg)
        else:
            self.log(f"Erro ao comprimir {file_path}")

    def decompress_single(self):
        file_path = filedialog.askopenfilename(filetypes=[("Huffman Files", "*.huff")])
        if not file_path: return
        
        out_path = file_path.replace(".huff", "_extracted.txt")
        res = subprocess.run([self.get_bin(), "-d", file_path, out_path])
        
        if res.returncode == 0:
            self.log(f"Sucesso: {os.path.basename(file_path)} extraído para {os.path.basename(out_path)}")
            messagebox.showinfo("Concluído", "Arquivo extraído com sucesso!")
        else:
            self.log(f"Erro ao extrair {file_path}")

    def batch_process(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        files = [f for f in os.listdir(folder) if f.endswith(".txt")]
        if not files:
            messagebox.showwarning("Aviso", "Nenhum arquivo .txt encontrado nesta pasta.")
            return

        self.batch_progress["maximum"] = len(files)
        self.batch_progress["value"] = 0
        
        for i, f in enumerate(files):
            in_p = os.path.join(folder, f)
            out_p = in_p + ".huff"
            self.batch_label.config(text=f"Processando: {f}")
            self.root.update()
            
            subprocess.run([self.get_bin(), "-c", in_p, out_p])
            
            self.batch_progress["value"] = i + 1
            self.log(f"Batch: {f} comprimido.")

        self.batch_label.config(text="Processamento em lote finalizado!")
        messagebox.showinfo("Batch", f"{len(files)} arquivos processados.")

    def clear_logs(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernHuffmanGUI(root)
    root.mainloop()