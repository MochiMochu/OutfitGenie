import tkinter as tk
from tkinter import ttk
import MenuHeader as header
from tkinter import filedialog
import UploadInfo
import CentreWindow as cw

class WardrobeMenu(tk.Frame):
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
        self.newItem = tk.PhotoImage(file="app-images/UploadItem.png")

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 800)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#ffdeed")
        self.header = header.MenuHeader(self.parent, self.window, "Wardrobe", "#ffdeed", self.close_and_open_home,
                                        self.close_and_open_generate, self.close_and_open_wardrobe,
                                        self.close_and_open_settings)
        self.header.pack()
        self.upload_items_button()

    def upload_items_button(self):
        self.buttonCont = ttk.Frame(self.window)
        self.uploadItemsBorder = tk.Frame(self.buttonCont,
                                          highlightbackground="#BDBDBD",
                                          highlightthickness=3,
                                          bd=0)
        self.generateOutfitsBtn = tk.Button(self.uploadItemsBorder,
                                            image=self.newItem,
                                            width=525,
                                            height=100,
                                            bd=0,
                                            relief="flat",
                                            command=self.upload_items_from_dir)
        self.generateOutfitsBtn.pack()
        self.uploadItemsBorder.pack()
        self.buttonCont.pack()

    def upload_items_from_dir(self):
        filepath = filedialog.askopenfilename(initialdir="This PC")
        with open("C:/Users/jasmi/PycharmProjects/OutfitGenie/app-text-files/image_paths.txt", "w") as file:
                file.write(filepath)
        self.upload_info()

    def upload_info(self):
        with open ("C:/Users/jasmi/PycharmProjects/OutfitGenie/app-text-files/image_paths.txt", "r") as f:
            path = f.readline()
            if len(path) != 0:
                upload_screen = UploadInfo.Popup(self.window, path)





