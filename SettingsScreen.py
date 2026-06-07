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
            variable=self.fullscreen_var,
            command=self.toggle_fullscreen,
            **BUTTON_SEVEN
        ).pack(anchor="w", pady=10)

        # nf
        res_frame = tk.Frame(panel, bg="white")
        res_frame.pack(anchor="w", pady=10)

        tk.Label(
            res_frame,
            text="Rozdzielczość:",
            **BUTTON_SEVEN
        ).pack(side="left")

        self.resolution_var = tk.StringVar(value="1200x800")
        resolutions = ["800x600", "1024x768", "1200x800", "1600x900", "1920x1080"]

        res_menu = tk.OptionMenu(
            res_frame,
            self.resolution_var,
            *resolutions,
            command=self.change_resolution  # Akcja po zmianie
        )
        res_menu.config(font=("Arial", 14), bg="white")
        res_menu.pack(side="left", padx=10)

        tk.Button(
            self,
            text="Powrót do menu",
            command=lambda: self.controller.show_frame("MenuScreen"),
            **BUTTON_SIX
        ).pack(pady=30)

    def toggle_fullscreen(self):
        # Pobieramy wartość
        is_fullscreen = self.fullscreen_var.get()
        self.controller.set_fullscreen(is_fullscreen)

    def change_resolution(self, selection):
        # Przekazanie
        self.controller.change_resolution(selection)

        if self.fullscreen_var.get():
            self.fullscreen_var.set(False)
            self.controller.set_fullscreen(False)