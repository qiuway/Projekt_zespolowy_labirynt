import tkinter as tk
from BaseScreen import BaseScreen


class CreditsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Autorzy")

        main_box = tk.Frame(self, bg="#e9e9e9")
        main_box.pack(anchor="n", pady=10)

        row = tk.Frame(main_box, bg="#e9e9e9")
        row.pack()

        def create_author_box(parent, title, description="Info o autorach"):
            box = tk.Frame(
                parent,
                bg="white",
                relief="solid",
                bd=3,
                padx=20,
                pady=20
            )
            box.pack(side="left", padx=60)

            tk.Label(
                box,
                text=title,
                font=("Arial", 18, "bold"),
                bg="white"
            ).pack(pady=(0, 10))

            tk.Label(
                box,
                text=description,
                font=("Arial", 14),
                bg="white",
                fg="gray"
            ).pack()

        create_author_box(row, "Filip")
        create_author_box(row, "Mikołaj")
        create_author_box(row, "Norbert")

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
        ).pack(pady=40)