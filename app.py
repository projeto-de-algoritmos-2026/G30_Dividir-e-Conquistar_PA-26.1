import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import traceback

COR_BG        = "#0F172A"  # Slate 900
COR_SURFACE   = "#1E293B"  # Slate 800
COR_CARD      = "#334155"  # Slate 700
COR_ACCENT    = "#38BDF8"  # Sky 400 (Ciano moderno)
COR_ACCENT2   = "#818CF8"  # Indigo 400
COR_TEXT      = "#F8FAFC"  # Slate 50
COR_TEXT_MUT  = "#94A3B8"  # Slate 400
COR_OK        = "#4ADE80"  # Green 400
COR_WARN      = "#FB7185"  # Rose 400

FONTE_TITULO  = ("Inter", 24, "bold")
FONTE_SUB     = ("Inter", 16, "bold")
FONTE_CORPO   = ("Inter", 12)
FONTE_SMALL   = ("Inter", 10)
FONTE_MONO    = ("JetBrains Mono", 11)

MOVIES_PATH   = os.path.join(os.path.dirname(__file__), "movies.json")


def carregar_filmes():
    try:
        with open(MOVIES_PATH, encoding="utf-8") as f:
            return json.load(f)["filmes"]
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo não encontrado:\n{MOVIES_PATH}")
        raise
    except json.JSONDecodeError as e:
        messagebox.showerror("Erro", f"JSON inválido em movies.json:\n{e}")
        raise


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Inversions — Análise de Afinidade")
        self.geometry("1024x768")
        self.resizable(True, True)
        self.configure(bg=COR_BG)
        self.minsize(900, 650)

        self._status_var = tk.StringVar(value="Pronto")
        status_bar = tk.Label(self, textvariable=self._status_var,
                               font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_BG,
                               anchor="e", padx=20, pady=10)
        status_bar.pack(side="bottom", fill="x")

        self.filmes         = carregar_filmes()
        self.n_pessoas      = tk.IntVar(value=2)
        self.pessoas        = []
        self.rankings       = {}
        self.n_filmes_sel   = tk.IntVar(value=5)
        self.filmes_sel     = []

        self.container = tk.Frame(self, bg=COR_BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._frames    = {}
        self._historico = []

        from tela_config    import TelaConfig
        from tela_avaliacao import TelaAvaliacao
        from tela_resultados import TelaResultados
        from tela_inversoes import TelaInversoes
        from tela_grafico   import TelaGrafico

        for Tela in (TelaConfig, TelaAvaliacao, TelaResultados, TelaInversoes, TelaGrafico):
            try:
                frame = Tela(self.container, self)
            except Exception as e:
                messagebox.showerror("Erro ao inicializar tela",
                                     f"{Tela.__name__}:\n{traceback.format_exc()}")
                self.destroy()
                return
            self._frames[Tela.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.bind("<Escape>", lambda e: self.voltar())
        
        self.mostrar("TelaConfig")

    def mostrar(self, nome: str):
        frame = self._frames.get(nome)
        if frame is None:
            messagebox.showerror("Erro", f"Tela '{nome}' não encontrada.")
            return
        try:
            if hasattr(frame, "ao_entrar"):
                frame.ao_entrar()
        except Exception:
            messagebox.showerror("Erro ao abrir tela",
                                 f"{nome}:\n{traceback.format_exc()}")
            return
        frame.tkraise()
        self._historico.append(nome)
        self._status_var.set(f"Sessão Ativa • {nome.replace('Tela','').strip()}")

    def voltar(self):
        if len(self._historico) > 1:
            self._historico.pop()
            destino = self._historico[-1]
            self._historico.pop()
            self.mostrar(destino)

    def set_status(self, msg: str):
        self._status_var.set(msg)

    @staticmethod
    def btn(parent, texto, comando, cor=COR_ACCENT, largura=18):
        return tk.Button(
            parent, text=texto, command=comando,
            bg=cor, fg=COR_BG, font=("Inter", 12, "bold"),
            relief="flat", bd=0, padx=20, pady=10,
            activebackground=COR_ACCENT2, activeforeground=COR_TEXT,
            cursor="hand2", width=largura
        )

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception:
        traceback.print_exc()
