import tkinter as tk
from BaseScreen import BaseScreen
from ButtonStyles import BUTTON_SIX
from ButtonStyles import BUTTON_SEVEN
from ButtonStyles import BUTTON_EIGHT

class SettingsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Ustawień")

        panel = tk.Frame(
            self,
            **BUTTON_EIGHT
        )
        panel.pack(pady=30)

        self.fullscreen_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            panel,
            text="Pełny ekran",
            **BUTTON_SEVEN
        ).pack(anchor="w", pady=10)

        tk.Checkbutton(
            panel,
            text="Muzyka",
            **BUTTON_SEVEN
        ).pack(anchor="w", pady=10)

        tk.Checkbutton(
            panel,
            text="Rozdzielczość",
            **BUTTON_SEVEN
        ).pack(anchor="w", pady=10)

        tk.Button(
            self,
            text="Powrót do menu",
            command=lambda: self.controller.show_frame("MenuScreen"),
            **BUTTON_SIX
        ).pack(pady=30)