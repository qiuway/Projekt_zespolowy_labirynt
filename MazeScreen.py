import tkinter as tk
import random
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
            text="Losowy labirynt",
            command=self.create_random_maze,
            **BUTTON_ONE
        ).pack(pady=6)

        tk.Button(
            left_panel,
            text="Zapisz labirynt",
            **BUTTON_ONE
        ).pack(pady=6)

        tk.Button(
            left_panel,
            text="Start",
            command=self.start_simulation,
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

    def create_random_maze(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())

            self.current_rows = max(10, min(40, rows))
            self.current_cols = max(10, min(40, cols))

            # Wypełnianie labiryntu ścianami
            self.grid_data = [
                [1 for _ in range(self.current_cols)]
                for _ in range(self.current_rows)
            ]

            old_start_pos = self.start_pos
            old_goal_pos = self.goal_pos

            # START
            if old_start_pos is not None:
                start_row, start_col = old_start_pos

                if 0 <= start_row < self.current_rows and 0 <= start_col < self.current_cols:
                    self.start_pos = old_start_pos
                else:
                    self.start_pos = (0, 0)
            else:
                self.start_pos = (0, 0)

            # META
            if old_goal_pos is not None:
                goal_row, goal_col = old_goal_pos

                if 0 <= goal_row < self.current_rows and 0 <= goal_col < self.current_cols:
                    self.goal_pos = old_goal_pos
                else:
                    self.goal_pos = (self.current_rows - 1, self.current_cols - 1)
            else:
                self.goal_pos = (self.current_rows - 1, self.current_cols - 1)

            # Start i meta nie mogą być na tym samym polu
            if self.start_pos == self.goal_pos:
                if self.start_pos != (self.current_rows - 1, self.current_cols - 1):
                    self.goal_pos = (self.current_rows - 1, self.current_cols - 1)
                else:
                    self.goal_pos = (0, 0)

            def is_inside(row, col):
                return 0 <= row < self.current_rows and 0 <= col < self.current_cols

            # Generowanie ścieżki
            def carve(row, col):
                self.grid_data[row][col] = 0

                directions = [
                    (-2, 0),
                    (2, 0),
                    (0, -2),
                    (0, 2)
                ]

                random.shuffle(directions)

                for dr, dc in directions:
                    new_row = row + dr
                    new_col = col + dc

                    if is_inside(new_row, new_col) and self.grid_data[new_row][new_col] == 1:
                        wall_row = row + dr // 2
                        wall_col = col + dc // 2

                        self.grid_data[wall_row][wall_col] = 0
                        self.grid_data[new_row][new_col] = 0

                        carve(new_row, new_col)

            # Rozpoczęcie generowania od lewego górnego rogu
            carve(0, 0)

            # Upewniamy się, że meta jest dostępna i połączona z labiryntem
            goal_row, goal_col = self.goal_pos
            self.grid_data[goal_row][goal_col] = 0

            possible_goal_connections = [
                (goal_row - 1, goal_col),
                (goal_row, goal_col - 1),
                (goal_row - 1, goal_col - 1),
            ]

            for r, c in possible_goal_connections:
                if 0 <= r < self.current_rows and 0 <= c < self.current_cols:
                    self.grid_data[r][c] = 0

            # Dodatkowe otwieranie pól, żeby było więcej rozgałęzień
            for row in range(self.current_rows):
                for col in range(self.current_cols):
                    if self.grid_data[row][col] == 1:
                        if random.random() < 0.10:
                            self.grid_data[row][col] = 0

            # Awaryjna droga w przypadku braku wygenerowanej ścieżki
            if not self.has_path():
                row, col = self.start_pos

                while row < self.current_rows:
                    self.grid_data[row][col] = 0
                    row += 1

                row -= 1

                while col < self.current_cols:
                    self.grid_data[row][col] = 0
                    col += 1

            self.size_label.config(
                text=f"Rozmiar:\n{self.current_rows} x {self.current_cols}"
            )

            if self.canvas:
                self.canvas.delete("all")

            start_row, start_col = self.start_pos
            goal_row, goal_col = self.goal_pos

            self.grid_data[start_row][start_col] = 0
            self.grid_data[goal_row][goal_col] = 0

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

    def start_simulation(self):
        if not self.validate_maze_path():
            return

        method = self.selected_method.get()
        path = []

        if method == "DFS":
            path = self.solve_dfs()
        elif method == "BFS":
            path = self.solve_bfs()
        elif method == "Prawej Ręki":
            path = self.solve_right_hand()

        if path:
            self.draw_final_path(path)
        else:
            messagebox.showinfo("Informacja", "Algorytm nie zwrócił ścieżki.")

    def draw_final_path(self, path):
        for row in range(self.current_rows):
            for col in range(self.current_cols):
                if self.grid_data[row][col] == 0 and (row, col) != self.start_pos and (row, col) != self.goal_pos:
                    self.canvas.itemconfig(f"cell_{row}_{col}", fill="white")

        for node in path:
            if node != self.start_pos and node != self.goal_pos:
                self.canvas.itemconfig(f"cell_{node[0]}_{node[1]}", fill="#f1c40f")  # Żółty kolor

    def solve_dfs(self):
        stack = [self.start_pos]
        parent = {self.start_pos: None}
        visited = {self.start_pos}

        while stack:
            curr = stack.pop()

            if curr == self.goal_pos:
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr]
                return path[::-1]

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if (0 <= nr < self.current_rows and 0 <= nc < self.current_cols and self.grid_data[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    stack.append((nr, nc))
        return []

    def solve_bfs(self):
        queue = deque([self.start_pos])
        parent = {self.start_pos: None}

        while queue:
            curr = queue.popleft()

            if curr == self.goal_pos:
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr]
                return path[::-1]

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if (0 <= nr < self.current_rows and 0 <= nc < self.current_cols and self.grid_data[nr][nc] == 0 and (nr, nc) not in parent):
                    parent[(nr, nc)] = curr
                    queue.append((nr, nc))
        return []

    def solve_right_hand(self):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        curr_pos = self.start_pos
        curr_dir = 1

        path = [curr_pos]
        # Maksymalna liczba krokow, aby uniknac nieskonczonej petli
        limit = self.current_rows * self.current_cols * 4

        for _ in range(limit):
            if curr_pos == self.goal_pos:
                return path

            found_move = False
            for i in [1, 0, -1, -2]:
                test_dir = (curr_dir + i) % 4
                dr, dc = directions[test_dir]
                nr, nc = curr_pos[0] + dr, curr_pos[1] + dc

                if 0 <= nr < self.current_rows and 0 <= nc < self.current_cols and self.grid_data[nr][nc] == 0:
                    curr_pos = (nr, nc)
                    curr_dir = test_dir
                    path.append(curr_pos)
                    found_move = True
                    break

            if not found_move: break
        return path

    def validate_maze_path(self):
        if not self.grid_data: return False

        rows, cols = self.current_rows, self.current_cols
        start, goal = self.start_pos, self.goal_pos

        queue = deque([start])
        visited = {start}
        found = False

        while queue:
            curr_r, curr_c = queue.popleft()
            if (curr_r, curr_c) == goal:
                found = True
                break

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr_r + dr, curr_c + dc
                if (0 <= nr < rows and 0 <= nc < cols and self.grid_data[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        if not found:
            messagebox.showwarning("Błąd", "Brak przejścia!")

        return found

    # Sprawdzanie możliwości przejścia
    def has_path(self):
        if not self.start_pos or not self.goal_pos:
            return False

        queue = deque([self.start_pos])
        visited = {self.start_pos}

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        while queue:
            row, col = queue.popleft()

            if (row, col) == self.goal_pos:
                return True

            for dr, dc in directions:
                new_row = row + dr
                new_col = col + dc

                if (
                        0 <= new_row < self.current_rows
                        and 0 <= new_col < self.current_cols
                        and (new_row, new_col) not in visited
                        and self.grid_data[new_row][new_col] == 0
                ):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))

        return False