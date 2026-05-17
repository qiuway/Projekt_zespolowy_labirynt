import tkinter as tk
from BaseScreen import BaseScreen

from ButtonStyles import BUTTON_SIX
from ButtonStyles import BUTTON_SEVEN
from ButtonStyles import BUTTON_NINE
from ButtonStyles import BUTTON_TEN

class CreditsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Autorzy")

        main_box = tk.Frame(self, bg="#e9e9e9")
        main_box.pack(anchor="n", pady=10)

        row = tk.Frame(main_box, bg="#e9e9e9")
        row.pack()

        def create_author_box(parent, title, description):
            box = tk.Frame(
                parent,
                **BUTTON_NINE
            )
            box.pack(side="left", padx=60)

            tk.Label(
                box,
                text=title,
                **BUTTON_SEVEN
            ).pack(pady=(0, 10))

            tk.Label(
                box,
                text=description,
                **BUTTON_TEN
            ).pack()

        create_author_box(row, "Filip Dorowski", "095867")
        create_author_box(row, "Mikołaj Kałczuga", "094057")
        create_author_box(row, "Norbert Fidler", "095905")

        tk.Button(
            self,
            text="Powrót do menu",
            command=lambda: self.controller.show_frame("MenuScreen"),
            **BUTTON_SIX
        ).pack(pady=40)