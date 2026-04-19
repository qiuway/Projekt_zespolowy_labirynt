import tkinter as tk
from tkinter import messagebox
from collections import deque

from BaseScreen import BaseScreen
from ButtonStyles import BUTTON_ONE
from ButtonStyles import BUTTON_TWO
from ButtonStyles import BUTTON_THREE
from ButtonStyles import BUTTON_FOUR

class MazeScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.validation = (self.register(self.validate_size), '%P')

        self.selected_method = tk.StringVar(value="DFS")
        self.rows_var = tk.StringVar(value="20")
        self.cols_var = tk.StringVar(value="20")

        # Nowa zmienna określająca, co aktualnie rysujemy na planszy
        self.draw_mode = tk.StringVar(value="Ściana")

        self.current_rows = None
        self.current_cols = None

        self.grid_data = []
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0

        # Zmienne przechowujące pozycje startu/mety
        self.start_pos = (0, 0)
        self.goal_pos = (0, 0)

        self.canvas = None
        self.method_label = None
        self.size_label = None

        self.create_title("Ekran Labiryntu")
        self.build_maze_ui()

    # walidacja wartosci wymiarow labiryntu
    def validate_size(self, new_value):
        if new_value == "":
            return True

        if new_value.isdigit():
            val = int(new_value)
            return val <= 40

        return False

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
            text="Rozmiar (10-40):",
            font=("Arial", 14),
            bg="#e9e9e9"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 6))

        tk.Entry(
            size_frame,
            textvariable=self.rows_var,
            width=5,
            justify="center",
            font=("Arial", 14),
            validate = "key",
            validatecommand = self.validation
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
            font=("Arial", 14),
            validate="key",
            validatecommand=self.validation
        ).grid(row=1, column=2)

        tk.Button(
            left_panel,
            text="Stwórz labirynt",
            command=self.create_maze,
            **BUTTON_ONE
        ).pack(pady=6)

        tk.Button(
            left_panel,
            text="Sprawdź labirynt",
            command=self.validate_maze_path,
            **BUTTON_ONE
        ).pack(pady=6)

        for text in ["Losowy labirynt", "Zapisz labirynt", "Start"]:
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

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", lambda e: self.on_canvas_click(e, erase=True))
        self.canvas.bind("<B3-Motion>", lambda e: self.on_canvas_click(e, erase=True))

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

        # Narzędzia
        tk.Label(
            right_panel,
            text="Narzędzie:",
            font=("Arial", 16, "bold"),
            bg="#e9e9e9"
        ).pack(pady=(20, 5))

        tools_frame = tk.Frame(right_panel, bg="#e9e9e9")
        tools_frame.pack(pady=(0, 15))

        for mode in ["Ściana", "Start", "Meta"]:
            tk.Radiobutton(
                tools_frame,
                text=mode,
                value=mode,
                variable=self.draw_mode,
                indicatoron=False,
                width=14,
                font=("Arial", 12),
                bg="white", fg="black", selectcolor="#dcdcdc", relief="solid", bd=2
            ).pack(pady=4)

    def update_method_label(self):
        self.method_label.config(text=f"Metoda:\n{self.selected_method.get()}")

    def create_maze(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())

            self.current_rows = max(10, min(40, rows))
            self.current_cols = max(10, min(40, cols))

            self.grid_data = [[0 for _ in range(self.current_cols)] for _ in range(self.current_rows)]

            # Domyślne pozycje start/meta
            self.start_pos = (0, 0)
            self.goal_pos = (self.current_rows - 1, self.current_cols - 1)

            self.size_label.config(text=f"Rozmiar:\n{self.current_rows} x {self.current_cols}")

            if self.canvas: self.canvas.delete("all")

            self.draw_grid()
        except ValueError:
            return

    def on_canvas_click(self, event, erase=False):
        if not self.grid_data: return

        col = int((event.x - self.offset_x) // self.cell_size)
        row = int((event.y - self.offset_y) // self.cell_size)

        if 0 <= row < self.current_rows and 0 <= col < self.current_cols:
            if erase:
                # Zabezpieczenie przed usunięciem punktu startu/mety
                if (row, col) != self.start_pos and (row, col) != self.goal_pos:
                    self.grid_data[row][col] = 0
            else:
                mode = self.draw_mode.get()

                if mode == "Ściana":
                    # Ściany nie można postawić na starcie/mecie
                    if (row, col) != self.start_pos and (row, col) != self.goal_pos:
                        self.grid_data[row][col] = 1
                elif mode == "Start":
                    # Startu nie można postawić na mecie
                    if (row, col) != self.goal_pos:
                        self.start_pos = (row, col)
                        self.grid_data[row][col] = 0  # Usuń ścianę jeśli tam była
                elif mode == "Meta":
                    # Mety nie można postawić na starcie
                    if (row, col) != self.start_pos:
                        self.goal_pos = (row, col)
                        self.grid_data[row][col] = 0  # Usuń ścianę jeśli tam była

            self.draw_grid()

    def redraw_current_grid(self, event=None):
        if self.grid_data:
            if self.canvas:
                self.canvas.delete("all")
            self.draw_grid()

    def draw_grid(self):
        if self.canvas is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 50 or canvas_height < 50:
            return

        margin = 20
        self.cell_size = min((canvas_width - 2 * margin) / self.current_cols,
                             (canvas_height - 2 * margin) / self.current_rows)

        self.offset_x = (canvas_width - (self.cell_size * self.current_cols)) / 2
        self.offset_y = (canvas_height - (self.cell_size * self.current_rows)) / 2

        # Rysuj wszystko od nowa TYLKO jeśli zmieniono rozmiar okna/labiryntu
        # Puste Canvas oznacza, że rysujemy pierwszy raz lub po zmianie rozmiaru
        if not self.canvas.find_all():
            for row in range(self.current_rows):
                for col in range(self.current_cols):
                    x1 = self.offset_x + col * self.cell_size
                    y1 = self.offset_y + row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size

                    color = "white"
                    if self.grid_data[row][col] == 1:
                        color = "#2c3e50"

                    if (row, col) == self.start_pos:
                        color = "#2ecc71"
                    elif (row, col) == self.goal_pos:
                        color = "#e74c3c"

                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline="black",
                        tags=f"cell_{row}_{col}"
                    )
        else:
            # Jeśli Canvas nie jest puste, aktualizujemy tylko kolory
            for row in range(self.current_rows):
                for col in range(self.current_cols):
                    color = "white"
                    if self.grid_data[row][col] == 1:
                        color = "#2c3e50"

                    if (row, col) == self.start_pos:
                        color = "#2ecc71"
                    elif (row, col) == self.goal_pos:
                        color = "#e74c3c"

                    self.canvas.itemconfig(f"cell_{row}_{col}", fill=color)

    def validate_maze_path(self):
        if not self.grid_data: return

        rows = self.current_rows
        cols = self.current_cols
        start = self.start_pos
        goal = self.goal_pos

        if self.grid_data[start[0]][start[1]] == 1 or self.grid_data[goal[0]][goal[1]] == 1:
            messagebox.showerror("Błąd", "Start lub Meta są zablokowane ścianą!")
            return

        queue = deque([start])
        visited = {start}

        while queue:
            curr_r, curr_c = queue.popleft()

            if (curr_r, curr_c) == goal:
                messagebox.showinfo("Sukces", "Labirynt jest prawidłowy! Istnieje droga do wyjścia.")
                return

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr_r + dr, curr_c + dc

                if (0 <= nr < rows and 0 <= nc < cols and self.grid_data[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        messagebox.showwarning("Błąd", "Brak przejścia! Labirynt jest nieprzejezdny.")