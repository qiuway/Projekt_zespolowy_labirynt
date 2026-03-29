import tkinter as tk
from ButtonStyles import BUTTON_ZERO

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e9e9e9")
        self.controller = controller

    def create_title(self, text):
        label = tk.Label(
            self,
            text=text,
            **BUTTON_ZERO
        )
        label.pack(pady=(20, 10))
        return label