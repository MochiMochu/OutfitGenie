import tkinter as tk
from tkinter import ttk
import MenuHeader as header
import CentreWindow as cw

class SettingsMenu(tk.Frame):
    def __init__(self, parent, open_home, open_generate, open_wardrobe, open_settings, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None
        self.close_app = close_app
        self.close_and_open_home = open_home
        self.close_and_open_generate = open_generate
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_settings = open_settings

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 800)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#f7d9c4")
        self.header = header.MenuHeader(self.parent, self.window, "Settings", "#f7d9c4", self.close_and_open_home,
                                        self.close_and_open_generate, self.close_and_open_wardrobe,
                                        self.close_and_open_settings)
        self.header.pack()
