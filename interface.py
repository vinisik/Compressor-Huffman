import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import time
from datetime import datetime
import random
import string

class AdvancedCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Compressão de Arquivos")
        self.root.geometry("800x650")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Sistema de Abas 
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_main = ttk.Frame(self.notebook)
        self.tab_batch = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_main, text=" Único Arquivo ")
        self.notebook.add(self.tab_batch, text=" Lotes/Gerar Arquivo ")
        self.notebook.add(self.tab_history, text=" Histórico/Logs ")
        
        # Configurar as abas
        self.setup_main_tab()
        self.setup_batch_tab()
        self.setup_history_tab()
        
        # Status bar global
        self.status_var = tk.StringVar(value="Aguardando operação...")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_main_tab(self):
        main_frame = ttk.Frame(self.tab_main, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_frame, text="Selecione a Operação", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Seleção de nível de compressão
        level_frame = ttk.Frame(main_frame)
        level_frame.pack(fill="x", pady=10)
        ttk.Label(level_frame, text="Nível de Compressão:").pack(side="left")
        
        self.level_var = tk.StringVar(value="1 - Rápido (Huffman)")
        self.level_cb = ttk.Combobox(level_frame, textvariable=self.level_var, state="readonly", width=35)
        self.level_cb['values'] = ("1 - Rápido (Huffman)", "2 - Máximo (LZW + Huffman)")
        self.level_cb.pack(side="left", padx=10)
        
        # Botões de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        self.btn_comp = ttk.Button(btn_frame, text="Comprimir Arquivo", command=self.start_compression)
        self.btn_comp.grid(row=0, column=0, padx=10, ipadx=10, ipady=5)
        
        self.btn_decomp = ttk.Button(btn_frame, text="Descompactar Arquivo", command=self.start_decompression)
        self.btn_decomp.grid(row=0, column=1, padx=10, ipadx=10, ipady=5)
        
        # Área de feedback (progresso real via C++ stdout)
        feedback_frame = ttk.LabelFrame(main_frame, text=" Estado da Operação ", padding="10")
        feedback_frame.pack(fill="x", pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(feedback_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=5)
        
        self.percent_label = ttk.Label(feedback_frame, text="0%")
        self.percent_label.pack(anchor="e")

        self.report_text = tk.Text(feedback_frame, height=4, state='disabled', bg="#f0f0f0")
        self.report_text.pack(fill="x", pady=5)

        # Tabela de Códigos Huffman (Preview)
        ttk.Label(main_frame, text="Tabela de Códigos Huffman (Preview):", font=("Arial", 10, "bold")).pack(pady=(15, 5), anchor="w")
        self.tree = ttk.Treeview(main_frame, columns=("Char", "ASCII", "Código"), show="headings", height=6)
        self.tree.heading("Char", text="Caráter")
        self.tree.heading("ASCII", text="Código ASCII")
        self.tree.heading("Código", text="Bits Huffman")
        self.tree.pack(expand=True, fill="both")

    def setup_batch_tab(self):
        frame = ttk.Frame(self.tab_batch, padding="20")
        frame.pack(expand=True, fill="both")
        
        # Processamento em lote
        ttk.Label(frame, text="Processamento em Lote (Batch)", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="Comprima todos os arquivos .txt de uma pasta selecionada.").pack()
        ttk.Button(frame, text="Selecionar Pasta e Comprimir", command=self.batch_process).pack(pady=10)
        
        self.batch_progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.batch_progress.pack(pady=10)
        self.batch_label = ttk.Label(frame, text="Aguardando...")
        self.batch_label.pack()
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Gerador de testes
        ttk.Label(frame, text="Gerador de arquivos de Teste", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="Crie arquivos grandes com redundância para testar a compressão.").pack()
        
        gen_frame = ttk.Frame(frame)
        gen_frame.pack(pady=10)
        
        ttk.Label(gen_frame, text="Tamanho (KB):").grid(row=0, column=0, padx=5)
        self.test_size_var = tk.StringVar(value="500")
        ttk.Entry(gen_frame, textvariable=self.test_size_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Button(gen_frame, text="Gerar arquivo...", command=self.gerar_teste).grid(row=0, column=2, padx=10)

    def setup_history_tab(self):
        frame = ttk.Frame(self.tab_history, padding="10")
        frame.pack(expand=True, fill="both")
        
        self.log_text = tk.Text(frame, state='disabled', font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.log_text.pack(expand=True, fill="both")
        
        ttk.Button(frame, text="Limpar Histórico", command=self.clear_logs).pack(pady=10)

    # Funções utilitárias
    def log(self, message):
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def clear_logs(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')

    def get_bin(self):
        return "./bin/huffman.exe" if os.name == 'nt' else "./bin/huffman"

    def toggle_buttons(self, state):
        mode = "normal" if state else "disabled"
        self.btn_comp.config(state=mode)
        self.btn_decomp.config(state=mode)
        self.level_cb.config(state=mode)

    def write_report(self, text):
        self.report_text.config(state='normal')
        self.report_text.delete('1.0', tk.END)
        self.report_text.insert(tk.END, text)
        self.report_text.config(state='disabled')

    def update_dict_preview(self, file_path):
        """Chama o binário C++ no modo -i para obter o dicionário Huffman gerado"""
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
                        if int(ascii_val) == 10: char_repr = "\\n (Quebra de linha)"
                        elif int(ascii_val) == 32: char_repr = "(Espaço)"
                        self.tree.insert("", tk.END, values=(char_repr, ascii_val, code))
                self.log(f"Pré-visualização do dicionário carregada para: {os.path.basename(file_path)}")
        except Exception as e:
            self.log(f"Aviso: Não foi possível gerar a pré-visualização. Erro: {e}")

    # Funções principais de compressão e ferramentas
    def gerar_teste(self):
        """Lógica para gerar arquivos massivos de teste"""
        try:
            tamanho_kb = int(self.test_size_var.get())
            if tamanho_kb <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Insira um tamanho válido em KB (inteiro positivo).")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"teste_{tamanho_kb}kb.txt", title="Guardar arquivo de Teste")
        if not file_path: return

        self.status_var.set("Gerando arquivo de teste...")
        self.root.update()

        try:
            caracteres = string.ascii_lowercase + " "
            pesos = [10 if c in 'aeiou ' else 1 for c in caracteres]
            conteudo = random.choices(caracteres, weights=pesos, k=tamanho_kb * 1024)
            
            with open(file_path, 'w') as f:
                f.write("".join(conteudo))
                
            self.log(f"Sucesso: Arquivo de teste gerado em {file_path} ({tamanho_kb} KB)")
            self.status_var.set("Pronto")
            messagebox.showinfo("Sucesso", f"Arquivo de {tamanho_kb}KB gerado com sucesso!")
        except Exception as e:
            self.log(f"Erro ao gerar teste: {str(e)}")
            messagebox.showerror("Erro", "Falha ao gerar o arquivo de teste.")

    def start_compression(self):
        file_path = filedialog.askopenfilename(title="Arquivo para Comprimir")
        if not file_path: return
        
        # Carregar a preview do dicionário
        self.update_dict_preview(file_path)
        
        # Iniciar a compressão multithread
        out_path = file_path + ".huff"
        level = "1" if "1" in self.level_var.get() else "2"
        
        self.toggle_buttons(False)
        self.progress_var.set(0)
        self.write_report("Processando...")
        self.log(f"Iniciando compressão de: {os.path.basename(file_path)}")
        
        threading.Thread(target=self.run_cpp_process, args=("-c", file_path, out_path, level), daemon=True).start()

    def start_decompression(self):
        file_path = filedialog.askopenfilename(title="Arquivo Huffman", filetypes=[("Huffman", "*.huff")])
        if not file_path: return
        
        out_path = file_path.replace(".huff", "_recuperado.txt")
        self.toggle_buttons(False)
        self.progress_var.set(0)
        self.write_report("Processando...")
        self.log(f"Iniciando descompressão de: {os.path.basename(file_path)}")
        
        threading.Thread(target=self.run_cpp_process, args=("-d", file_path, out_path, "1"), daemon=True).start()

    def batch_process(self):
        """Processamento em lote na segunda aba"""
        folder = filedialog.askdirectory()
        if not folder: return
        
        files = [f for f in os.listdir(folder) if f.endswith(".txt")]
        if not files:
            messagebox.showwarning("Aviso", "Nenhum arquivo .txt encontrado na pasta.")
            return

        self.batch_progress["maximum"] = len(files)
        self.batch_progress["value"] = 0
        self.log(f"Iniciando processamento em lote de {len(files)} arquivos no diretório: {folder}")
        
        start_t = time.time()
        for i, f in enumerate(files):
            in_p = os.path.join(folder, f)
            out_p = in_p + ".huff"
            self.batch_label.config(text=f"Processando: {f}")
            self.root.update()
            
            subprocess.run([self.get_bin(), "-c", in_p, out_p])
            
            self.batch_progress["value"] = i + 1
            self.log(f"Batch - Concluído: {f}")

        total_time = time.time() - start_t
        self.batch_label.config(text="Processamento em lote finalizado!")
        self.log(f"Processamento em lote finalizado em {total_time:.2f}s.")
        messagebox.showinfo("Lote Concluído", f"{len(files)} arquivos processados com sucesso!")

    # Comunicação com o C++ 
    def run_cpp_process(self, mode, input_file, output_file, level):
        try:
            start_time = time.time()
            
            # Popen permite ler a saída do C++ linha a linha em tempo real
            process = subprocess.Popen(
                [self.get_bin(), mode, input_file, output_file, level],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
            )

            if process.stdout is not None:
                for line in process.stdout:
                    line = line.strip()
                    if line.startswith("PROGRESS:"):
                        percent = int(line.split(":")[1])
                        self.root.after(0, self.update_progress, percent)
                    elif line.startswith("INFO:"):
                        msg = line.split(":")[1]
                        self.root.after(0, self.update_status, msg)
                    elif line.startswith("ERRO:"):
                        self.root.after(0, self.update_status, "Ocorreu um erro!")
                        break

            process.wait()
            end_time = time.time()

            if process.returncode == 0:
                self.root.after(0, self.finish_success, mode, input_file, output_file, end_time - start_time)
            else:
                error_msg = process.stderr.read() if process.stderr else "Erro desconhecido (sem saída de erro)."
                self.root.after(0, self.show_error, error_msg)

        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.root.after(0, self.toggle_buttons, True)

    def update_progress(self, percent):
        self.progress_var.set(percent)
        self.percent_label.config(text=f"{percent}%")

    def update_status(self, msg):
        self.status_var.set(msg)

    def finish_success(self, mode, original, output, duration):
        self.update_progress(100)
        self.update_status("Concluído com sucesso!")
        
        size_in = os.path.getsize(original)
        size_out = os.path.getsize(output)
        
        if mode == "-c":
            ratio = (1 - (size_out / size_in)) * 100
            report = f"Estatísticas:\nOriginal: {size_in/1024:.2f} KB | Comprimido: {size_out/1024:.2f} KB\nEconomia: {ratio:.2f}%\nTempo: {duration:.2f} s"
            self.log(f"Sucesso: Compressão concluída. Economia de {ratio:.2f}%.")
        else:
            report = f"Descompressão concluída!\nTamanho recuperado: {size_out/1024:.2f} KB\nTempo: {duration:.2f} segundos"
            self.log(f"Sucesso: Descompressão concluída.")
            
        self.write_report(report)
        messagebox.showinfo("Sucesso", "Operação finalizada com sucesso!")

    def show_error(self, error_msg):
        self.update_status("Falha na operação.")
        self.log(f"ERRO: {error_msg}")
        messagebox.showerror("Erro C++", f"O motor de compressão falhou:\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCompressorGUI(root)
    root.mainloop()