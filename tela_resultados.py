import tkinter as tk
from tkinter import ttk
from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)
from inversions import total_inversoes_grupo, similaridade

class TelaResultados(tk.Frame):
    """Mostra ranking agregado dos filmes e sumário de afinidade."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._build()

    def _build(self):
        # Cabeçalho
        header = tk.Frame(self, bg=COR_BG, pady=25)
        header.pack(fill="x")
        tk.Label(header, text="Análise de Preferências", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()

        # Rodapé
        footer = tk.Frame(self, bg=COR_BG, pady=25)
        footer.pack(fill="x", padx=40)

        tk.Button(footer, text="← Voltar", command=self.app.voltar,
                  bg=COR_SURFACE, fg=COR_TEXT, font=FONTE_SMALL,
                  relief="flat", padx=20, pady=10).pack(side="left")
