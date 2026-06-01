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
        pessoas = self.app.pessoas
        pares = [f"{pessoas[i]} × {pessoas[j]}"
                 for i in range(len(pessoas))
                 for j in range(i+1, len(pessoas))]
        self._combo["values"] = pares
        if pares:
            self._combo.current(0)
            self._mostrar_par()

    def _mostrar_par(self):
        for w in self._inner.winfo_children():
            w.destroy()

        val = self._par_var.get()
        if " × " not in val:
            return
        pa, pb = val.split(" × ")

        ra = self.app.rankings[pa]
        rb = self.app.rankings[pb]
        filmes = self.app.filmes_sel

        num_inv, pares_inv = contar_inversoes(ra, rb)
        sim = similaridade(num_inv, len(filmes))

        # Sumário do Par
        sumario = tk.Frame(self._inner, bg=COR_SURFACE, padx=25, pady=20)
        sumario.pack(fill="x", pady=(0, 20))

        tk.Label(sumario, text=f"Total: {num_inv} Inversões", font=("Inter", 14, "bold"),
                 fg=COR_ACCENT, bg=COR_SURFACE).pack(side="right")

        tk.Label(sumario, text=f"A afinidade entre {pa} e {pb} é de {sim}%", font=FONTE_CORPO,
                 fg=COR_TEXT, bg=COR_SURFACE).pack(anchor="w")

        tk.Label(sumario,
                 text="O algoritmo detectou que vocês discordam na ordem de preferência dos pares abaixo:",
                 font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_SURFACE).pack(anchor="w", pady=(5, 0))

        # Lista de Inversões
        if not pares_inv:
            tk.Label(self._inner, text="Nenhuma inversão encontrada! Vocês têm o mesmo gosto. 🎉",
                     font=FONTE_CORPO, fg=COR_OK, bg=COR_BG).pack(pady=40)
        else:
            for i, j in pares_inv:
                self._card_inversao(filmes[i], filmes[j], pa, pb,
                                    ra[i], ra[j], rb[i], rb[j])

    def _card_inversao(self, f1, f2, p1, p2, n1_1, n1_2, n2_1, n2_2):
        card = tk.Frame(self._inner, bg=COR_SURFACE, padx=20, pady=15)
        card.pack(fill="x", pady=5)

        tk.Label(card, text=f"Divergência: {f1['titulo']} vs {f2['titulo']}",
                 font=("Inter", 11, "bold"), fg=COR_WARN, bg=COR_SURFACE).pack(anchor="w")

        pref1 = f1['titulo'] if n1_1 > n1_2 else f2['titulo']
        pref2 = f1['titulo'] if n2_1 > n2_2 else f2['titulo']

        container_detalhe = tk.Frame(card, bg=COR_SURFACE, pady=5)
        container_detalhe.pack(fill="x")

        tk.Label(container_detalhe, text=f"• {p1} prefere {pref1}",
                 font=FONTE_SMALL, fg=COR_TEXT, bg=COR_SURFACE).pack(anchor="w")
        tk.Label(container_detalhe, text=f"• {p2} prefere {pref2}",
                 font=FONTE_SMALL, fg=COR_TEXT, bg=COR_SURFACE).pack(anchor="w")

        notas_txt = f"(Notas {p1}: {n1_1} e {n1_2} | Notas {p2}: {n2_1} e {n2_2})"
        tk.Label(card, text=notas_txt, font=("Inter", 8), fg=COR_TEXT_MUT,
                 bg=COR_SURFACE).pack(anchor="w")

