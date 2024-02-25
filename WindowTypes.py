import tkinter as tk
from tkinter import ttk
import CentreWindow as cw
from rembg import remove
from PIL import Image, ImageChops
import tkinter.font as tkfont
import sqlite3
from datetime import datetime
import os


class UserValidation(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, *kwargs)
        self.parent = parent
        self.style = ttk.Style()
        self.window = None

        # variables needed for switching between windows

        # variables needed to hold values of input boxes
        self.username = None
        self.email = None
        self.password = None
        self.confirm_password = None
        self.location = None


class PopUpWindows(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.style = ttk.Style()
        self.window = None

        self.exitButton = None





