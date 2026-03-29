import tkinter as tk
from BaseScreen import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Ustawień")

        panel = tk.Frame(
            self,
            bg="white",
            relief="solid",
            bd=3,
            padx=30,
            pady=30
        )
        panel.pack(pady=30)

        self.fullscreen_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            panel,
            text="Pełny ekran",
            variable=self.fullscreen_var,
            font=("Arial", 18),
            bg="white"
        ).pack(anchor="w", pady=10)

        tk.Checkbutton(
            panel,
            text="Muzyka",
            font=("Arial", 18),
            bg="white"
        ).pack(anchor="w", pady=10)

        tk.Checkbutton(
            panel,
            text="Rozdzielczość",
            font=("Arial", 18),
            bg="white"
        ).pack(anchor="w", pady=10)

        tk.Button(
            self,
            text="Powrót do menu",
            font=("Arial", 16),
            bg="white",
            fg="black",
            relief="solid",
            bd=3,
            width=16,
            height=2,
            command=lambda: self.controller.show_frame("MenuScreen")
        ).pack(pady=30)