import tkinter as tk

from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)
from inversions import total_inversoes_grupo, similaridade

class TelaGrafico(tk.Frame):
    """Visualização única do Heatmap de Similaridade com contagem de inversões."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._build()

    def _build(self):
        # Cabeçalho
        header = tk.Frame(self, bg=COR_BG, pady=20)
        header.pack(fill="x")

        tk.Label(header, text="Matriz de Afinidade", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()
        tk.Label(header, text="Afinidade (%) e Número de Inversões detectadas",
                 font=FONTE_CORPO, fg=COR_TEXT_MUT, bg=COR_BG).pack(pady=(5, 0))

        # Canvas vazio — preenchido em ao_entrar
        self.container_grafico = tk.Frame(self, bg=COR_SURFACE, bd=0)
        self.container_grafico.pack(fill="both", expand=True, padx=40, pady=10)

        self.cv = tk.Canvas(self.container_grafico, bg=COR_SURFACE,
                            highlightthickness=0, cursor="cross")
        self.cv.pack(fill="both", expand=True, padx=20, pady=20)

        # Rodapé com botões de navegação
        footer = tk.Frame(self, bg=COR_BG, pady=20)
        footer.pack(fill="x", padx=40)

        tk.Button(footer, text="← Voltar para Resultados",
                  command=self.app.voltar,
                  bg=COR_CARD, fg=COR_TEXT, font=FONTE_SMALL,
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left")

        tk.Button(footer, text="Ver Detalhes das Inversões  →",
                  command=lambda: self.app.mostrar("TelaInversoes"),
                  bg=COR_ACCENT2, fg=COR_TEXT, font=("Inter", 10, "bold"),
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="right")

    def ao_entrar(self):
        pass
