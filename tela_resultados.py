import tkinter as tk
from tkinter import ttk
from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)
from inversions import total_inversoes_grupo, similaridade

MEDALHAS = ["🥇", "🥈", "🥉"] + ["•"] * 20

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

        # Área de conteúdo (scroll)
        container = tk.Frame(self, bg=COR_BG)
        container.pack(fill="both", expand=True, padx=40)

        canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(canvas, bg=COR_BG)
        win_id = canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        # Rodapé
        footer = tk.Frame(self, bg=COR_BG, pady=25)
        footer.pack(fill="x", padx=40)

        tk.Button(footer, text="← Voltar", command=self.app.voltar,
                  bg=COR_SURFACE, fg=COR_TEXT, font=FONTE_SMALL,
                  relief="flat", padx=20, pady=10).pack(side="left")
        tk.Button(footer, text="Ver Matriz de Afinidade  →",
                  command=lambda: self.app.mostrar("TelaGrafico"),
                  bg=COR_ACCENT, fg=COR_BG, font=("Inter", 11, "bold"),
                  relief="flat", padx=25, pady=10, cursor="hand2").pack(side="right")

    def ao_entrar(self):
        for w in self._inner.winfo_children():
            w.destroy()

        rankings = self.app.rankings
        filmes   = self.app.filmes_sel
        n_pessoas = len(self.app.pessoas)

        # Calcula nota média por filme e ordena
        medias = []
        for i, filme in enumerate(filmes):
            notas = [rankings[p][i] for p in self.app.pessoas]
            media = sum(notas) / n_pessoas
            medias.append((filme, notas, media))
        medias.sort(key=lambda x: x[2], reverse=True)

        # Seção: Ranking Agregado
        self._sec_titulo("🏆  Consenso do Grupo")
        for pos, (filme, notas, media) in enumerate(medias):
            self._card_filme(pos, filme, notas, media)
        
                # Seção: Destaques de Afinidade
        resultado_grupo = total_inversoes_grupo(rankings)
        if resultado_grupo:
            self._sec_titulo("✨  Destaques de Afinidade")
            stats_frame = tk.Frame(self._inner, bg=COR_BG)
            stats_frame.pack(fill="x", pady=10)

            par_max = max(resultado_grupo, key=lambda k: resultado_grupo[k][0])
            par_min = min(resultado_grupo, key=lambda k: resultado_grupo[k][0])

            self._card_stat(stats_frame, "Mais Sintonizados",
                            f"{par_min[0]} & {par_min[1]}", COR_OK)
            self._card_stat(stats_frame, "Mais Divergentes",
                            f"{par_max[0]} & {par_max[1]}", COR_WARN)

    def _sec_titulo(self, texto):
        f = tk.Frame(self._inner, bg=COR_BG)
        f.pack(fill="x", pady=(20, 10))
        tk.Label(f, text=texto, font=FONTE_SUB, fg=COR_ACCENT, bg=COR_BG, anchor="w").pack(fill="x")

    def _card_filme(self, pos, filme, notas, media):
        card = tk.Frame(self._inner, bg=COR_SURFACE, padx=20, pady=15)
        card.pack(fill="x", pady=5)

        medalha = MEDALHAS[pos] if pos < len(MEDALHAS) else "•"

        lbl_info = tk.Frame(card, bg=COR_SURFACE)
        lbl_info.pack(side="left", fill="both", expand=True)

        tk.Label(lbl_info, text=f"{medalha}  {filme['titulo']}",
                 font=("Inter", 13, "bold"), fg=COR_TEXT, bg=COR_SURFACE, anchor="w").pack(fill="x")
        tk.Label(lbl_info, text=f"{filme['diretor']} • {filme['ano']}",
                 font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_SURFACE, anchor="w").pack(fill="x")

        tk.Label(card, text=f"{media:.1f}", font=("Inter", 18, "bold"),
                 fg=COR_ACCENT, bg=COR_SURFACE).pack(side="right", padx=10)
    def _card_stat(self, parent, titulo, nomes, cor):
        card = tk.Frame(parent, bg=COR_SURFACE, padx=20, pady=15)
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(card, text=titulo, font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_SURFACE).pack(anchor="w")
        tk.Label(card, text=nomes, font=("Inter", 12, "bold"), fg=cor, bg=COR_SURFACE).pack(anchor="w", pady=(2, 0))
