import tkinter as tk
from tkinter import ttk


class SettingsMenu(tk.Frame):
    def __init__(self, parent, open_home, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None
        self.close_app = close_app

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#ddedea")
        label = tk.Label(text="Settings Screen")
        label.pack()
