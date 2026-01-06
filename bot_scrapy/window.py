import tkinter as tk
from tkinter import ttk
import requests
from dotenv import load_dotenv
import os
import webbrowser


# =========================
# CATEGORIAS
# =========================
class CategoriesFrame(ttk.LabelFrame):
    def __init__(self, parent, categories):
        super().__init__(parent, text="CATEGORIAS", padding=10)
        self.categories = categories
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

            category_id = category["id"]
            category_name = category["name"]

            self.variables[category_id] = var

            ttk.Checkbutton(scrollable_frame, text=category_name, variable=var).grid(
                row=i, column=0, sticky="w", pady=5
            )


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

        ttk.Entry(self, textvariable=self.page_var, width=30).grid(
            row=1, column=0, pady=(0, 15), sticky="ew"
        )

        ttk.Label(self, text="Desconto mínimo (%):").grid(row=2, column=0, sticky="w")

        ttk.Entry(self, textvariable=self.discount_var, width=30).grid(
            row=3, column=0, sticky="ew"
        )

        self.columnconfigure(0, weight=1)


# =========================
# BOTÕES
# =========================
class ButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=(0, 10))
        self._build_ui()

    def _build_ui(self):
        tk.Button(
            self,
            text="Iniciar",
            bg="#2e7d32",
            fg="white",
            activebackground="#1b5e20",
            relief="flat",
            padx=18,
            pady=8,
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            self,
            text="Reiniciar",
            bg="#c62828",
            fg="white",
            activebackground="#8e0000",
            relief="flat",
            padx=18,
            pady=8,
        ).pack(side="left")


# =========================
# LOGS
# =========================
class LogsFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="LOGS", padding=10)
        self._build_ui()
        self._insert_fake_logs()

    def _truncate_text(self, text, max_length=50):
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    def _build_ui(self):
        self.columnconfigure(0, weight=3)  # 30%
        self.columnconfigure(1, weight=7)  # 70%
        self.rowconfigure(0, weight=1)

        # ==========================
        # LEFT LOG (30%)
        # ==========================
        left_container = ttk.Frame(self)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_container.rowconfigure(1, weight=1)

        # --------------------------
        # STATUS ATUAL
        # --------------------------
        status_frame = ttk.Frame(left_container)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)

        self._status_line(status_frame, 0, "🔄", "Categoria atual: Ração seca")
        self._status_line(
            status_frame,
            1,
            "🔗",
            "Link atual: https://www.mercadolivre.com.br/mais-vendidos/MLB1144",
            link="https://www.mercadolivre.com.br/mais-vendidos/MLB1144",
        )
        self._status_line(status_frame, 2, "📦", "Produtos criados: 128")
        self._status_line(status_frame, 3, "♻️", "Produtos atualizados: 42")

        # --------------------------
        # CATEGORIAS PROCESSADAS (SCROLL)
        # --------------------------
        processed_frame = ttk.LabelFrame(left_container, text="CATEGORIAS PROCESSADAS")
        processed_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        processed_frame.columnconfigure(0, weight=1)
        processed_frame.columnconfigure(1, weight=0)

        processed_frame.configure(height=140)
        processed_frame.pack_propagate(False)

        self.processed_text = tk.Text(
            processed_frame,
            bg="#1e1e1e",
            fg="#e0e0e0",
            font=("Consolas", 10),
            wrap="word",
            height=7,
        )

        scrollbar = ttk.Scrollbar(
            processed_frame, orient="vertical", command=self.processed_text.yview
        )

        self.processed_text.configure(yscrollcommand=scrollbar.set)

        self.processed_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.processed_text.config(state="disabled")

        # ==========================
        # RIGHT LOG (70%)
        # ==========================
        self.main_log = tk.Text(
            self,
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="none",
        )
        self.main_log.grid(row=0, column=1, sticky="nsew")
        self.main_log.config(state="disabled")


    def _status_line(self, parent, row, emoji, text, link=None):
        # Emoji
        tk.Label(
            parent,
            text=emoji,
            font=("Segoe UI Emoji", 11),
            bg="#1e1e1e",
            anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=(0, 6))

        # Texto (sempre criado)
        if link:
            display_text = self._truncate_text(text, 55)

            label = tk.Label(
                parent,
                text=display_text,
                font=("Consolas", 10),
                fg="#64b5f6",
                bg="#1e1e1e",
                cursor="hand2",
                anchor="w",
                justify="left"
            )

            label.bind(
                "<Button-1>",
                lambda e, url=link: webbrowser.open(url)
            )
        else:
            label = tk.Label(
                parent,
                text=text,
                font=("Consolas", 10),
                fg="#e0e0e0",
                bg="#1e1e1e",
                anchor="w",
                justify="left",
                wraplength=260
            )


        label.grid(row=row, column=1, sticky="w")
        
    def _insert_fake_logs(self):
        # --------------------------
        # CATEGORIAS PROCESSADAS
        # --------------------------
        processed = [
            "✅ Brinquedos",
            "✅ Antipulgas",
            "✅ Coleiras",
            "✅ Camas e almofadas",
            "✅ Areia sanitária",
            "⏳ Ração seca",
        ]

        self.processed_text.config(state="normal")
        for item in processed:
            self.processed_text.insert("end", item + "\n")
        self.processed_text.config(state="disabled")

        # --------------------------
        # LOG PRINCIPAL
        # --------------------------
        logs = [
            "2026-01-05 21:34:11,102 | INFO     | app.startup        | Application started",
            "2026-01-05 21:34:11,451 | INFO     | config.loader      | Environment variables loaded",
            "2026-01-05 21:34:12,087 | INFO     | api.client         | Fetching categories from API",
            "2026-01-05 21:34:12,842 | INFO     | api.client         | 15 categories received",
            "2026-01-05 21:34:13,003 | WARNING  | api.client         | Category 'Antipulgas' marked as inactive",
            "2026-01-05 21:34:13,221 | INFO     | ui.categories      | Categories rendered successfully",
            "2026-01-05 21:34:14,019 | ERROR    | api.client         | Connection timeout after 10 seconds",
            "2026-01-05 21:34:14,020 | INFO     | app.idle           | Waiting for user action...",
        ]

        self.main_log.config(state="normal")
        for line in logs:
            self.main_log.insert("end", line + "\n")
        self.main_log.see("end")
        self.main_log.config(state="disabled")


# =========================
# APP
# =========================
class App(tk.Tk):
    load_dotenv()
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Raspagem de produtos")
        self.geometry("1000x650")
        self.state("zoomed")
        self.resizable(True, True)
        self.configure(bg="#1e1e1e")

        self._configure_style()

        self.categories = self._load_categories()

        self._build_layout()

    def _load_categories(self):
        response = requests.get(
            f"{self.API_URL}/api/categories/",
            headers={
                "Authorization": f"Api-Key {self.API_KEY}",
                "Accept": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("TFrame", background="#1e1e1e")

        style.configure("TLabelframe", background="#1e1e1e", foreground="#e0e0e0")

        style.configure(
            "TLabelframe.Label",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
        )

        style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0")

        style.configure("TCheckbutton", background="#1e1e1e", foreground="#e0e0e0")

        style.configure("TEntry", fieldbackground="#2b2b2b", foreground="#ffffff")

    def _build_layout(self):
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        top = ttk.Frame(main)
        top.pack(fill="both", expand=False)

        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)

        CategoriesFrame(top, self.categories).grid(
            row=0, column=0, sticky="nsew", padx=(0, 10)
        )

        ParametersFrame(top).grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ButtonsFrame(main).pack(anchor="w", pady=(12, 18))
        LogsFrame(main).pack(fill="both", expand=True)


if __name__ == "__main__":
    App().mainloop()
