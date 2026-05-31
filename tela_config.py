import tkinter as tk
from tkinter import ttk, messagebox
from app import (COR_BG, COR_SURFACE, COR_CARD, COR_ACCENT, COR_ACCENT2,
                 COR_TEXT, COR_TEXT_MUT, COR_OK, COR_WARN,
                 FONTE_TITULO, FONTE_SUB, FONTE_CORPO, FONTE_SMALL)


class TelaConfig(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COR_BG)
        self.app = app
        self._vars_nomes = []
        self._vars_filmes = []
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COR_BG, pady=40)
        header.pack(fill="x")
        tk.Label(header, text="Cinema Inversions", font=FONTE_TITULO,
                 fg=COR_TEXT, bg=COR_BG).pack()
        tk.Label(header, text="Análise algorítmica de afinidade cinematográfica",
                 font=FONTE_CORPO, fg=COR_TEXT_MUT, bg=COR_BG).pack(pady=(5, 0))

        container = tk.Frame(self, bg=COR_BG)
        container.pack(fill="both", expand=True, padx=60)

        canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(canvas, bg=COR_BG)
        self._win_id = canvas.create_window((0, 0), window=self._inner, anchor="nw")
        
        self._inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            self._win_id, width=e.width))

        self._sec_pessoas()
        self._sec_filmes()
        
        footer = tk.Frame(self, bg=COR_BG, pady=40)
        footer.pack(fill="x", padx=60)
        
        tk.Button(footer, text="Começar Avaliação  →",
                  command=self._avancar,
                  bg=COR_ACCENT, fg=COR_BG, font=("Inter", 12, "bold"),
                  relief="flat", padx=30, pady=12, cursor="hand2").pack(side="right")

    def _sec_pessoas(self):
        pad = tk.Frame(self._inner, bg=COR_BG)
        pad.pack(fill="x", pady=(0, 30))

        tk.Label(pad, text="Pessoas", font=FONTE_SUB,
                 fg=COR_ACCENT, bg=COR_BG, anchor="w").pack(fill="x")
        
        row = tk.Frame(pad, bg=COR_BG, pady=15)
        row.pack(fill="x")
        tk.Label(row, text="Quantos avaliadores?", font=FONTE_CORPO,
                 fg=COR_TEXT, bg=COR_BG).pack(side="left")

        spin = tk.Spinbox(row, from_=2, to=10, width=5, textvariable=self.app.n_pessoas,
                          font=FONTE_CORPO, bg=COR_SURFACE, fg=COR_TEXT,
                          buttonbackground=COR_CARD, relief="flat", bd=5,
                          command=self._atualizar_nomes)
        spin.pack(side="left", padx=15)
        self.app.n_pessoas.trace_add("write", lambda *_: self._atualizar_nomes())

        self._frame_nomes = tk.Frame(pad, bg=COR_BG)
        self._frame_nomes.pack(fill="x")
        self._atualizar_nomes()

    def _atualizar_nomes(self):
        for w in self._frame_nomes.winfo_children():
            w.destroy()
        self._vars_nomes.clear()

        try:
            n = int(self.app.n_pessoas.get())
        except: return

        grid = tk.Frame(self._frame_nomes, bg=COR_BG)
        grid.pack(fill="x")
        
        for i in range(n):
            var = tk.StringVar(value=f"Avaliador {i+1}")
            self._vars_nomes.append(var)
            
            r, c = divmod(i, 2)
            cell = tk.Frame(grid, bg=COR_BG, pady=5)
            cell.grid(row=r, column=c, sticky="ew", padx=(0 if c==0 else 10, 0))
            grid.columnconfigure(c, weight=1)
            
            tk.Entry(cell, textvariable=var, font=FONTE_CORPO,
                     bg=COR_SURFACE, fg=COR_TEXT, insertbackground=COR_TEXT,
                     relief="flat", bd=8).pack(fill="x")

    def _sec_filmes(self):
        pad = tk.Frame(self._inner, bg=COR_BG)
        pad.pack(fill="x", pady=10)

        tk.Label(pad, text="Seleção de Filmes", font=FONTE_SUB,
                 fg=COR_ACCENT, bg=COR_BG, anchor="w").pack(fill="x")
        
        tk.Label(pad, text="Escolha os filmes para o ranking (2-10):",
                 font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_BG, anchor="w").pack(fill="x", pady=(5, 15))

        grid = tk.Frame(pad, bg=COR_BG)
        grid.pack(fill="x")
        self._vars_filmes.clear()

        for idx, filme in enumerate(self.app.filmes):
            var = tk.BooleanVar(value=(idx < 5))
            self._vars_filmes.append(var)
            
            r, c = divmod(idx, 2)
            cell = tk.Frame(grid, bg=COR_SURFACE, padx=15, pady=12)
            cell.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
            grid.columnconfigure(c, weight=1)
            
            cb = tk.Checkbutton(cell, text=f" {filme['titulo']}",
                                 variable=var, font=("Inter", 11, "bold"),
                                 fg=COR_TEXT, bg=COR_SURFACE, selectcolor=COR_BG,
                                 activebackground=COR_SURFACE, activeforeground=COR_ACCENT,
                                 cursor="hand2")
            cb.pack(anchor="w")
            tk.Label(cell, text=f"   {filme['diretor']} • {filme['ano']}",
                     font=FONTE_SMALL, fg=COR_TEXT_MUT, bg=COR_SURFACE).pack(anchor="w")

    def _avancar(self):
        nomes = [v.get().strip() for v in self._vars_nomes]
        if any(not n for n in nomes):
            messagebox.showwarning("Atenção", "Preencha todos os nomes.")
            return
        
        selecionados = [f for f, v in zip(self.app.filmes, self._vars_filmes) if v.get()]
        if not (2 <= len(selecionados) <= 10):
            messagebox.showwarning("Atenção", "Selecione entre 2 e 10 filmes.")
            return

        self.app.pessoas     = nomes
        self.app.filmes_sel  = selecionados
        self.app.rankings    = {}
        self.app.mostrar("TelaAvaliacao")

    def ao_entrar(self):
        self._atualizar_nomes()
