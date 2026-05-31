"""
tela_avaliacao.py — Tela 2: cada pessoa atribui notas (1-10) a cada filme.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)


class TelaAvaliacao(tk.Frame):
    """Tela de avaliação: um aba por pessoa, sliders de nota por filme."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._tabs = {}
        self._build()

    def _build(self):
        # Cabeçalho
        header = tk.Frame(self, bg=COR_BG, pady=30)
        header.pack(fill="x")
        tk.Label(header, text="Avaliação", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()
        tk.Label(header, text="Atribua notas aos filmes selecionados",
                 font=FONTE_CORPO, fg=COR_TEXT_MUT, bg=COR_BG).pack(pady=(5, 0))

        # Área central para o Notebook
        self._area = tk.Frame(self, bg=COR_BG)
        self._area.pack(fill="both", expand=True, padx=60)

        # Rodapé
        footer = tk.Frame(self, bg=COR_BG, pady=30)
        footer.pack(fill="x", padx=60)
        
        tk.Button(footer, text="← Voltar", command=self.app.voltar,
                  bg=COR_SURFACE, fg=COR_TEXT, font=FONTE_SMALL,
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left")
        
        tk.Button(footer, text="Gerar Análise  →", command=self._avancar,
                  bg=COR_ACCENT, fg=COR_BG, font=("Inter", 11, "bold"),
                  relief="flat", padx=25, pady=10, cursor="hand2").pack(side="right")

    def ao_entrar(self):
        for w in self._area.winfo_children():
            w.destroy()
        self._tabs.clear()

        # Estilo do Notebook Moderno
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=COR_SURFACE, foreground=COR_TEXT_MUT,
                         font=("Inter", 10, "bold"), padding=[20, 10])
        style.map("TNotebook.Tab",
                  background=[("selected", COR_ACCENT)],
                  foreground=[("selected", COR_BG)])

        nb = ttk.Notebook(self._area)
        nb.pack(fill="both", expand=True)

        for pessoa in self.app.pessoas:
            tab_frame = tk.Frame(nb, bg=COR_BG)
            nb.add(tab_frame, text=f"  {pessoa.upper()}  ")
            self._tabs[pessoa] = {}
            self._build_tab(tab_frame, pessoa)

    def _build_tab(self, parent, pessoa):
        canvas = tk.Canvas(parent, bg=COR_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COR_BG)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        for filme in self.app.filmes_sel:
            fid = filme["id"]
            nota_var = tk.DoubleVar(value=5.0)
            self._tabs[pessoa][fid] = nota_var

            card = tk.Frame(inner, bg=COR_SURFACE, padx=25, pady=20)
            card.pack(fill="x", pady=10)

            # Info Filme
            tk.Label(card, text=filme["titulo"], font=("Inter", 12, "bold"),
                     fg=COR_TEXT, bg=COR_SURFACE, anchor="w").pack(fill="x")
            
            # Slider de Nota
            slider_row = tk.Frame(card, bg=COR_SURFACE, pady=10)
            slider_row.pack(fill="x")

            lbl_nota = tk.Label(slider_row, text="5.0", font=("Inter", 14, "bold"),
                                 fg=COR_ACCENT, bg=COR_SURFACE, width=3)
            lbl_nota.pack(side="right", padx=(15, 0))

            slider = tk.Scale(
                slider_row, variable=nota_var, from_=1, to=10,
                resolution=0.5, orient="horizontal", showvalue=False,
                bg=COR_SURFACE, fg=COR_ACCENT, troughcolor=COR_BG,
                activebackground=COR_ACCENT, highlightthickness=0,
                command=lambda v, lbl=lbl_nota: lbl.config(text=f"{float(v):.1f}")
            )
            slider.pack(side="left", fill="x", expand=True)

    def _avancar(self):
        rankings = {}
        for pessoa in self.app.pessoas:
            notas = [self._tabs[pessoa][f["id"]].get() for f in self.app.filmes_sel]
            rankings[pessoa] = notas

        self.app.rankings = rankings
        self.app.mostrar("TelaResultados")
