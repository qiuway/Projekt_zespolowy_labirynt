import tkinter as tk
from tkinter import filedialog, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Labirynty")
        self.geometry("1200x800")
        self.configure(bg="#e9e9e9")
        self.fullscreen = False

        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (MenuScreen, MazeScreen, SettingsScreen, CreditsScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(MenuScreen)
        self.bind("<Escape>", self.exit_fullscreen)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_fullscreen(self, value: bool):
        self.fullscreen = value
        self.attributes("-fullscreen", value)

    def exit_fullscreen(self, event=None):
        self.set_fullscreen(False)
        settings_frame = self.frames[SettingsScreen]
        settings_frame.fullscreen_var.set(False)


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


class MenuScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Menu")

        center_frame = tk.Frame(self, bg="#e9e9e9")
        center_frame.pack(expand=True)

        buttons = [
            ("Start", lambda: controller.show_frame(MazeScreen)),
            ("Ustawienia", lambda: controller.show_frame(SettingsScreen)),
            ("Credits", lambda: controller.show_frame(CreditsScreen)),
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


class MazeScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.selected_method = tk.StringVar(value="DFS")
        self.edit_mode = tk.BooleanVar(value=False)
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
            command=lambda: self.controller.show_frame(MenuScreen)
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

        canvas.create_text(
            400, 250,
            text="",
            fill="white",
            font=("Arial", 24, "bold")
        )

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


class SettingsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Ustawień")

        panel = tk.Frame(
            self,
            bg="white",
            relief="solid",
            bd=3,
            padx=30,
            pady=30
        )
        panel.pack(pady=30)

        self.fullscreen_var = tk.BooleanVar(value=False)

        fullscreen_check = tk.Checkbutton(
            panel,
            text="Pełny ekran",
            variable=self.fullscreen_var,
            font=("Arial", 18),
            bg="white"
        )
        fullscreen_check.pack(anchor="w", pady=10)

        sound_var = tk.BooleanVar(value=True)
        sound_check = tk.Checkbutton(
            panel,
            text="Muzyka",
            variable=sound_var,
            font=("Arial", 18),
            bg="white"
        )
        sound_check.pack(anchor="w", pady=10)

        resolution_var = tk.BooleanVar(value=True)
        resolution_check = tk.Checkbutton(
            panel,
            text="Rozdzielczość",
            variable=resolution_var,
            font=("Arial", 18),
            bg="white"
        )
        resolution_check.pack(anchor="w", pady=10)

        hints_var = tk.BooleanVar(value=False)
        hints_check = tk.Checkbutton(
            panel,
            text="",
            variable=hints_var,
            font=("Arial", 18),
            bg="white"
        )

        back_btn = tk.Button(
            self,
            text="Powrót do menu",
            font=("Arial", 16),
            bg="white",
            fg="black",
            relief="solid",
            bd=3,
            width=16,
            height=2,
            command=lambda: self.controller.show_frame(MenuScreen)
        )
        back_btn.pack(pady=30)


class CreditsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_title("Ekran Credits")

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
            command=lambda: self.controller.show_frame(MenuScreen)
        ).pack(pady=40)


if __name__ == "__main__":
    app = App()
    app.mainloop()