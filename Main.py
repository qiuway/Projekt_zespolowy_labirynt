import tkinter as tk

from MenuScreen import MenuScreen
from MazeScreen import MazeScreen
from SettingsScreen import SettingsScreen
from CreditsScreen import CreditsScreen


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

        screens = {
            "MenuScreen": MenuScreen,
            "MazeScreen": MazeScreen,
            "SettingsScreen": SettingsScreen,
            "CreditsScreen": CreditsScreen,
        }

        for name, ScreenClass in screens.items():
            frame = ScreenClass(container, self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("MenuScreen")
        self.bind("<Escape>", self.exit_fullscreen)

    def show_frame(self, frame_name):
        self.frames[frame_name].tkraise()

    def set_fullscreen(self, value: bool):
        self.fullscreen = value
        self.attributes("-fullscreen", value)

    def exit_fullscreen(self, event=None):
        self.set_fullscreen(False)
        settings_frame = self.frames["SettingsScreen"]
        settings_frame.fullscreen_var.set(False)


if __name__ == "__main__":
    app = App()
    app.mainloop()