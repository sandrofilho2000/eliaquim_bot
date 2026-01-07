import tkinter as tk
from tkinter import ttk
import requests
from dotenv import load_dotenv
import os
import webbrowser
from scraper.categories import Categories

# =========================
# CATEGORIAS
# =========================
class CategoriesFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="CATEGORIAS", padding=10)
        categories_service = Categories()
        self.categories = categories_service._load_categories()
        self.variables = {}
        self._build_ui()

    def _build_ui(self):
        canvas = tk.Canvas(self, highlightthickness=0, bg="#1E1E1E")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, category in enumerate(self.categories):
            var = tk.BooleanVar(value=category.get("active", False))
            self.variables[category["id"]] = var

            ttk.Checkbutton(
                scrollable_frame,
                text=category["name"],
                variable=var
            ).grid(row=i, column=0, sticky="w", pady=5)

    def get_active_categories(self):
        return [
            category["name"]
            for category in self.categories
            if self.variables[category["id"]].get()
        ]


# =========================
# PARÂMETROS
# =========================
class ParametersFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="PARÂMETROS", padding=15)
        self.page_var = tk.StringVar(value="3")
        self.discount_var = tk.StringVar(value="20")
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Ir até a página:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.page_var).grid(
            row=1, column=0, pady=(0, 15), sticky="ew"
        )

        ttk.Label(self, text="Desconto mínimo (%):").grid(row=2, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.discount_var).grid(
            row=3, column=0, sticky="ew"
        )

        self.columnconfigure(0, weight=1)


# =========================
# LOGS
# =========================
class LogsFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="LOGS", padding=10)
        self._build_ui()
        self._insert_fake_logs()

    def _build_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=7)
        self.rowconfigure(0, weight=1)

        left_container = ttk.Frame(self)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_container.rowconfigure(1, weight=1)

        status_frame = ttk.Frame(left_container)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self._status_line(status_frame, 0, "🔄", "Categoria atual: Ração seca")
        self._status_line(
            status_frame,
            1,
            "🔗",
            "Link atual: https://www.mercadolivre.com.br/mais-vendidos/MLB1144",
            link="https://www.mercadolivre.com.br/mais-vendidos/MLB1144",
        )

        processed_frame = ttk.LabelFrame(left_container, text="CATEGORIAS PROCESSADAS")
        processed_frame.grid(row=1, column=0, sticky="ew")

        self.processed_text = tk.Text(
            processed_frame,
            bg="#1e1e1e",
            fg="#e0e0e0",
            font=("Consolas", 10),
            height=7,
            state="disabled",
        )
        self.processed_text.pack(fill="both", expand=True)

        self.main_log = tk.Text(
            self,
            bg="#1e1e1e",
            fg="#e0e0e0",
            font=("Consolas", 10),
            state="disabled",
        )
        self.main_log.grid(row=0, column=1, sticky="nsew")

    def _status_line(self, parent, row, emoji, text, link=None):
        tk.Label(parent, text=emoji, bg="#1e1e1e").grid(row=row, column=0, sticky="w")

        label = tk.Label(
            parent,
            text=text,
            fg="#64b5f6" if link else "#e0e0e0",
            bg="#1e1e1e",
            cursor="hand2" if link else "",
            wraplength=260,
            justify="left",
        )

        if link:
            label.bind("<Button-1>", lambda e: webbrowser.open(link))

        label.grid(row=row, column=1, sticky="w")

    def add_log(self, message):
        self.main_log.config(state="normal")
        self.main_log.insert("end", message + "\n")
        self.main_log.see("end")
        self.main_log.config(state="disabled")

    def _insert_fake_logs(self):
        self.add_log("Application started")
        self.add_log("Waiting for user action...")


# =========================
# BOTÕES
# =========================
class ButtonsFrame(ttk.Frame):
    def __init__(self, parent, categories_frame, logs_frame):
        super().__init__(parent, padding=(0, 10))
        self.categories_frame = categories_frame
        self.logs_frame = logs_frame
        self._build_ui()

    def _build_ui(self):
        tk.Button(
            self,
            text="Iniciar",
            bg="#2e7d32",
            fg="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self._on_start,
        ).pack(side="left", padx=(0, 12))

    def _on_start(self):
        categories = self.categories_frame.get_active_categories()

        if not categories:
            self.logs_frame.add_log("⚠️ Nenhuma categoria ativa selecionada.")
            return

        self.logs_frame.add_log("\n\n▶️ Iniciando processamento:")
        for cat in categories:
            self.logs_frame.add_log(f"• {cat}")


# =========================
# APP
# =========================
class App(tk.Tk):
    load_dotenv()
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")

    def __init__(self):
        super().__init__()
        self._configure_style()
        self.title("Raspagem de produtos")
        self.state("zoomed")
        self.configure(bg="#1e1e1e")
        self._build_layout()

    def _build_layout(self):
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        # =========================
        # TOP: CATEGORIAS + PARÂMETROS
        # =========================
        top = ttk.Frame(main)
        top.pack(fill="x")

        self.categories_frame = CategoriesFrame(top)
        self.categories_frame.pack(
            side="left", fill="both", expand=True, padx=(0, 10)
        )

        ParametersFrame(top).pack(
            side="left", fill="both", expand=True
        )

        # =========================
        # LOGS (CRIADO ANTES)
        # =========================
        self.logs_frame = LogsFrame(main)

        # =========================
        # CONTROLS: BOTÕES
        # =========================
        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=(12, 12))

        ButtonsFrame(
            controls,
            self.categories_frame,
            self.logs_frame
        ).pack(anchor="w")

        # =========================
        # LOGS (ÚNICO COM EXPAND)
        # =========================
        self.logs_frame.pack(fill="both", expand=True)




    def _configure_style(self):
        style = ttk.Style(self)

        # Tema que respeita dark mode
        style.theme_use("clam")

        style.configure("TFrame", background="#1e1e1e")

        style.configure(
            "TLabelframe",
            background="#1e1e1e",
            foreground="#e0e0e0"
        )

        style.configure(
            "TLabelframe.Label",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="#e0e0e0"
        )

        style.configure(
            "TCheckbutton",
            background="#1e1e1e",
            foreground="#e0e0e0"
        )

        style.map(
            "TCheckbutton",
            background=[("active", "#1e1e1e")],
            foreground=[("active", "#ffffff")]
        )

        style.configure(
            "TEntry",
            fieldbackground="#2b2b2b",
            foreground="#ffffff",
            insertcolor="white"
        )

if __name__ == "__main__":
    App().mainloop()
