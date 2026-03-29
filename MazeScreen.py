import tkinter as tk
from BaseScreen import BaseScreen


class MazeScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.selected_method = tk.StringVar(value="DFS")
        self.rows_var = tk.StringVar(value="20")
        self.cols_var = tk.StringVar(value="20")

        self.create_title("Ekran Labiryntu")
        self.build_maze_ui()

    def build_maze_ui(self):
        outer = tk.Frame(self, bg="#e9e9e9")
        outer.pack(fill="both", expand=True, padx=20, pady=10)

        top_panel = tk.Frame(outer, bg="#e9e9e9")
        top_panel.pack(fill="x", pady=(0, 10))

        tk.Button(
            top_panel,
            text="Powrót do menu",
            font=("Arial", 14),
            bg="white",
            relief="solid",
            bd=3,
            width=16,
            command=lambda: self.controller.show_frame("MenuScreen")
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            top_panel,
            text="Metoda:",
            font=("Arial", 16, "bold"),
            bg="#e9e9e9"
        ).pack(side="left", padx=(20, 5))

        for method in ["DFS", "BFS", "Prawej Ręki"]:
            tk.Radiobutton(
                top_panel,
                text=method,
                value=method,
                variable=self.selected_method,
                indicatoron=False,
                font=("Arial", 14),
                bg="white",
                selectcolor="#dcdcdc",
                relief="solid",
                bd=3,
                width=12,
                pady=8
            ).pack(side="left", padx=5)

        middle = tk.Frame(outer, bg="#e9e9e9")
        middle.pack(fill="both", expand=True)

        left_panel = tk.Frame(middle, bg="#e9e9e9", width=220)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="Tworzenie labiryntu",
            font=("Arial", 18, "bold"),
            bg="#e9e9e9"
        ).pack(pady=(10, 15))

        size_frame = tk.Frame(left_panel, bg="#e9e9e9")
        size_frame.pack(pady=(0, 15))

        tk.Label(size_frame, text="Rozmiar:", font=("Arial", 14), bg="#e9e9e9").grid(row=0, column=0, columnspan=3)

        tk.Entry(size_frame, textvariable=self.rows_var, width=5, justify="center").grid(row=1, column=0)
        tk.Label(size_frame, text="x", bg="#e9e9e9").grid(row=1, column=1)
        tk.Entry(size_frame, textvariable=self.cols_var, width=5, justify="center").grid(row=1, column=2)

        for text in [
            "Stwórz labirynt",
            "Losowy labirynt",
            "Edytuj labirynt",
            "Zapisz labirynt",
            "Start"
        ]:
            tk.Button(
                left_panel,
                text=text,
                font=("Arial", 14),
                bg="white",
                relief="solid",
                bd=3,
                width=16,
                height=2
            ).pack(pady=6)

        center_panel = tk.Frame(middle, bg="#e9e9e9")
        center_panel.pack(side="left", fill="both", expand=True)

        canvas_frame = tk.Frame(center_panel, bg="black", bd=4, relief="solid")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(canvas_frame, bg="black")
        canvas.pack(fill="both", expand=True)

        right_panel = tk.Frame(middle, bg="#e9e9e9", width=220)
        right_panel.pack(side="left", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)

        tk.Label(
            right_panel,
            text="Informacje",
            font=("Arial", 18, "bold"),
            bg="#e9e9e9"
        ).pack(pady=(10, 15))

        tk.Label(
            right_panel,
            text="Metoda:\nDFS",
            font=("Arial", 14),
            bg="white",
            relief="solid",
            bd=3,
            width=16,
            height=3
        ).pack(pady=8)

        tk.Label(
            right_panel,
            text="Rozmiar:\n20 x 20",
            font=("Arial", 14),
            bg="white",
            relief="solid",
            bd=3,
            width=16,
            height=3
        ).pack(pady=8)