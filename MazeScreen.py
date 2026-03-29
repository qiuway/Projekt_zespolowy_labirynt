import tkinter as tk

from BaseScreen import BaseScreen
from ButtonStyles import BUTTON_ONE
from ButtonStyles import BUTTON_TWO
from ButtonStyles import BUTTON_THREE
from ButtonStyles import BUTTON_FOUR

class MazeScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.selected_method = tk.StringVar(value="DFS")
        self.rows_var = tk.StringVar(value="20")
        self.cols_var = tk.StringVar(value="20")

        self.current_rows = None
        self.current_cols = None

        self.canvas = None
        self.method_label = None
        self.size_label = None

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
            command=lambda: self.controller.show_frame("MenuScreen"),
            **BUTTON_THREE
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
                command=self.update_method_label,
                **BUTTON_FOUR
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

        tk.Label(
            size_frame,
            text="Rozmiar:",
            font=("Arial", 14),
            bg="#e9e9e9"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 6))

        tk.Entry(
            size_frame,
            textvariable=self.rows_var,
            width=5,
            justify="center",
            font=("Arial", 14)
        ).grid(row=1, column=0)

        tk.Label(
            size_frame,
            text="x",
            font=("Arial", 14, "bold"),
            bg="#e9e9e9"
        ).grid(row=1, column=1, padx=5)

        tk.Entry(
            size_frame,
            textvariable=self.cols_var,
            width=5,
            justify="center",
            font=("Arial", 14)
        ).grid(row=1, column=2)

        tk.Button(
            left_panel,
            text="Stwórz labirynt",
            command=self.create_maze,
            **BUTTON_ONE
        ).pack(pady=6)

        for text in ["Losowy labirynt", "Edytuj labirynt", "Zapisz labirynt", "Start"]:
            tk.Button(
                left_panel,
                text=text,
                **BUTTON_ONE
            ).pack(pady=6)

        center_panel = tk.Frame(middle, bg="#e9e9e9")
        center_panel.pack(side="left", fill="both", expand=True)

        canvas_frame = tk.Frame(center_panel, bg="black", bd=4, relief="solid")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self.redraw_current_grid)

        right_panel = tk.Frame(middle, bg="#e9e9e9", width=220)
        right_panel.pack(side="left", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)

        tk.Label(
            right_panel,
            text="Informacje",
            font=("Arial", 18, "bold"),
            bg="#e9e9e9"
        ).pack(pady=(10, 15))

        self.method_label = tk.Label(
            right_panel,
            text="Metoda:\nDFS",
            **BUTTON_TWO
        )
        self.method_label.pack(pady=8)

        self.size_label = tk.Label(
            right_panel,
            text="Rozmiar:\nBrak",
            **BUTTON_TWO
        )
        self.size_label.pack(pady=8)

    def update_method_label(self):
        self.method_label.config(text=f"Metoda:\n{self.selected_method.get()}")

    def create_maze(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
        except ValueError:
            return

        self.current_rows = rows
        self.current_cols = cols
        self.size_label.config(text=f"Rozmiar:\n{rows} x {cols}")
        self.draw_grid(rows, cols)

    def redraw_current_grid(self, event=None):
        if self.current_rows is not None and self.current_cols is not None:
            self.draw_grid(self.current_rows, self.current_cols)

    def draw_grid(self, rows, cols):
        if self.canvas is None:
            return

        self.canvas.delete("all")
        self.canvas.update_idletasks()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 50 or canvas_height < 50:
            return

        margin = 20
        usable_width = canvas_width - 2 * margin
        usable_height = canvas_height - 2 * margin

        cell_size = min(usable_width / cols, usable_height / rows)

        grid_width = cell_size * cols
        grid_height = cell_size * rows

        start_x = (canvas_width - grid_width) / 2
        start_y = (canvas_height - grid_height) / 2

        for row in range(rows):
            for col in range(cols):
                x1 = start_x + col * cell_size
                y1 = start_y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="white",
                    outline="black"
                )