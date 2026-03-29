import tkinter as tk


class BaseScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e9e9e9")
        self.controller = controller

    def create_title(self, text):
        label = tk.Label(
            self,
            text=text,
            font=("Arial", 28, "bold"),
            bg="#e9e9e9",
            fg="black"
        )
        label.pack(pady=(20, 10))
        return label

    def menu_button(self, text, command, width=18, height=2, font_size=16):
        return tk.Button(
            self,
            text=text,
            font=("Arial", font_size),
            bg="white",
            fg="black",
            relief="solid",
            bd=3,
            width=width,
            height=height,
            command=command
        )