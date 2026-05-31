import tkinter as tk
from tkinter import ttk

from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)
from inversions import contar_inversoes, similaridade
class TelaInversoes(tk.Frame):
    """Exibe os pares invertidos entre cada dupla de avaliadores."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._par_var = tk.StringVar()
        self._build()

    def _build(self):
        # Cabeçalho
        header = tk.Frame(self, bg=COR_BG, pady=25)
        header.pack(fill="x")
        tk.Label(header, text="Detalhamento de Inversões", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()

        # Seletor de par
        sel_frame = tk.Frame(self, bg=COR_SURFACE, pady=15, padx=30)
        sel_frame.pack(fill="x", padx=60, pady=10)

        tk.Label(sel_frame, text="Comparando:", font=FONTE_SMALL,
                 fg=COR_TEXT_MUT, bg=COR_SURFACE).pack(side="left")

        self._combo = ttk.Combobox(sel_frame, textvariable=self._par_var,
                                   state="readonly", font=FONTE_CORPO, width=30)
        self._combo.pack(side="left", padx=15)

        # Área de scroll para os cards de inversão
        container = tk.Frame(self, bg=COR_BG)
        container.pack(fill="both", expand=True, padx=60)

        canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(canvas, bg=COR_BG)
        win_id = canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        # Rodapé
        footer = tk.Frame(self, bg=COR_BG, pady=25)
        footer.pack(fill="x", padx=60)

        tk.Button(footer, text="← Voltar para Gráfico", command=self.app.voltar,
                  bg=COR_SURFACE, fg=COR_TEXT, font=FONTE_SMALL,
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left")

    def ao_entrar(self):
        pass
