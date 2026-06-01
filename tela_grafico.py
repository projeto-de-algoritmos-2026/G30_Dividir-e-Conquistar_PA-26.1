import tkinter as tk
from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)
from inversions import total_inversoes_grupo, similaridade


def _lerp_cor(t, cor_a=COR_WARN, cor_b=COR_OK):
    """Interpola linearmente entre duas cores hexadecimais para o heatmap.

    t=0 → cor_a (discordante/vermelho)
    t=1 → cor_b (sintonizado/verde)
    """
    def h2rgb(c):
        c = c.lstrip("#")
        return [int(c[i:i+2], 16) for i in (0, 2, 4)]

    ra, ga, ba = h2rgb(cor_a)
    rb, gb, bb = h2rgb(cor_b)
    r = int(ra + (rb - ra) * t)
    g = int(ga + (gb - ga) * t)
    b = int(ba + (bb - ba) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class TelaGrafico(tk.Frame):
    """Visualização única do Heatmap de Similaridade com contagem de inversões."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._build()

    def _build(self):
        # Cabeçalho Moderno
        header = tk.Frame(self, bg=COR_BG, pady=20)
        header.pack(fill="x")

        tk.Label(header, text="Matriz de Afinidade", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()
        tk.Label(header, text="Afinidade (%) e Número de Inversões detectadas",
                 font=FONTE_CORPO, fg=COR_TEXT_MUT, bg=COR_BG).pack(pady=(5, 0))

        # Área Principal do Gráfico
        self.container_grafico = tk.Frame(self, bg=COR_SURFACE, bd=0)
        self.container_grafico.pack(fill="both", expand=True, padx=40, pady=10)

        self.cv = tk.Canvas(self.container_grafico, bg=COR_SURFACE,
                            highlightthickness=0, cursor="cross")
        self.cv.pack(fill="both", expand=True, padx=20, pady=20)

        # Rodapé com controles
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
        self.update_idletasks()
        self._desenhar_heatmap()

    def _desenhar_heatmap(self):
        cv = self.cv
        cv.delete("all")

        rankings = self.app.rankings
        pessoas  = self.app.pessoas
        n_filmes = len(self.app.filmes_sel)
        resultado = total_inversoes_grupo(rankings)

        W = cv.winfo_width()
        H = cv.winfo_height()
        n = len(pessoas)

        if n == 0:
            return

        # Cálculo de dimensões dinâmicas
        margin_left = 120
        margin_top = 60
        available_w = W - margin_left - 40
        available_h = H - margin_top - 120

        cell_size = min(available_w // n, available_h // n, 120)

        # Centralização da grade
        offset_x = margin_left + (available_w - cell_size * n) // 2
        offset_y = margin_top + (available_h - cell_size * n) // 2

        # Labels dos nomes (eixos X e Y)
        for i, nome in enumerate(pessoas):
            x = offset_x + i * cell_size + cell_size // 2
            cv.create_text(x, offset_y - 20, text=nome, fill=COR_TEXT,
                           font=("Inter", 10, "bold"))

            y = offset_y + i * cell_size + cell_size // 2
            cv.create_text(offset_x - 15, y, text=nome, fill=COR_TEXT,
                           font=("Inter", 10, "bold"), anchor="e")

        # Células da matriz
        for i in range(n):
            for j in range(n):
                x0 = offset_x + j * cell_size
                y0 = offset_y + i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                if i == j:
                    cv.create_rectangle(x0, y0, x1, y1, fill=COR_CARD,
                                        outline=COR_SURFACE, width=2)
                    cv.create_text((x0+x1)//2, (y0+y1)//2, text="—",
                                   fill=COR_TEXT_MUT, font=FONTE_CORPO)
                else:
                    pi, pj = pessoas[i], pessoas[j]
                    key = (pi, pj) if (pi, pj) in resultado else (pj, pi)

                    if key in resultado:
                        inv = resultado[key][0]
                        sim = similaridade(inv, n_filmes)
                        cor = _lerp_cor(sim / 100)

                        cv.create_rectangle(x0, y0, x1, y1, fill=cor,
                                            outline=COR_SURFACE, width=2)

                        cor_texto = "#000000" if sim > 60 else COR_TEXT
                        cv.create_text((x0+x1)//2, (y0+y1)//2 - 10,
                                       text=f"{sim:.0f}%",
                                       fill=cor_texto, font=("Inter", 11, "bold"))
                        cv.create_text((x0+x1)//2, (y0+y1)//2 + 12,
                                       text=f"{inv} inv.",
                                       fill=cor_texto, font=("Inter", 9))
                    else:
                        cv.create_rectangle(x0, y0, x1, y1, fill=COR_CARD,
                                            outline=COR_SURFACE)

        # Legenda Informativa
        leg_y = H - 50
        cv.create_text(W//2, leg_y - 20,
                       text="Como ler: % é a afinidade | 'inv' é o total de discordâncias (inversões)",
                       fill=COR_TEXT_MUT, font=FONTE_SMALL)

        leg_w = 200
        leg_h = 8
        leg_x = (W - leg_w) // 2

        for i in range(leg_w):
            t = i / leg_w
            cor = _lerp_cor(t)
            cv.create_line(leg_x + i, leg_y, leg_x + i, leg_y + leg_h, fill=cor)

        cv.create_text(leg_x - 10, leg_y + 4, text="Discordantes",
                       fill=COR_WARN, font=FONTE_SMALL, anchor="e")
        cv.create_text(leg_x + leg_w + 10, leg_y + 4, text="Sintonizados",
                       fill=COR_OK, font=FONTE_SMALL, anchor="w")
