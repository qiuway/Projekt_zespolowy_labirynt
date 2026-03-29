import tkinter as tk
from BaseScreen import BaseScreen


class MenuScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Menu")

        center_frame = tk.Frame(self, bg="#e9e9e9")
        center_frame.pack(expand=True)

        buttons = [
            ("Start", lambda: controller.show_frame("MazeScreen")),
            ("Ustawienia", lambda: controller.show_frame("SettingsScreen")),
            ("Autorzy", lambda: controller.show_frame("CreditsScreen")),
            ("Wyjście", controller.destroy),
        ]

        for text, command in buttons:
            btn = tk.Button(
                center_frame,
                text=text,
                font=("Arial", 20),
                bg="white",
                fg="black",
                relief="solid",
                bd=3,
                width=20,
                height=2,
                command=command
            )
            btn.pack(pady=12)