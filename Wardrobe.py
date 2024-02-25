import tkinter as tk
from tkinter import ttk
import MenuHeader as header
from tkinter import filedialog
import UploadInfo
import CentreWindow as cw
import ItemViewer as itemview
import OutfitViewer as outfitview


class WardrobeMenu(tk.Frame):
    def __init__(self, parent, open_home, open_generate, open_wardrobe, open_settings, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.style = ttk.Style()
        self.window = None

        # variables to track presence of pop up windows
        self.upload_item_window = None
        self.view_item_window = None
        self.view_outfit_window = None

        # creating tkinter photoImages for the buttons
        self.newItem = tk.PhotoImage(file="app-images/UploadItem.png")
        self.viewItem = tk.PhotoImage(file="app-images/ViewItem.png")
        self.viewOutfit = tk.PhotoImage(file="app-images/ViewOutfit.png")

        # assigns variable names to functions to switch between the windows
        self.close_app = close_app
        self.close_and_open_home = open_home
        self.close_and_open_generate = open_generate
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_settings = open_settings

        # creates variables to hold widgets
        self.header = None
        self.upperButtonCont = None
        self.uploadItemsBorder = None
        self.generateOutfitsBtn = None
        self.lowerButtonCont = None
        self.viewItemsBorder = None
        self.viewItemsBtn = None
        self.viewOutfitsBorder = None
        self.viewOutfitsBtn = None
        self.uploadErrorFrame = None
        self.uploadError = None

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

    # creates button to open a pop up window for uploading new items
    def upload_items_button(self):
        self.style.configure("Wardrobe.TFrame", background="#ffdeed")
        self.upperButtonCont = ttk.Frame(self.window, style="Wardrobe.TFrame")
        self.uploadItemsBorder = tk.Frame(self.upperButtonCont,
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

        self.lowerButtonCont = ttk.Frame(self.window, style="Wardrobe.TFrame")
        self.viewItemsBorder = tk.Frame(self.lowerButtonCont,
                                        highlightbackground="#BDBDBD",
                                        highlightthickness=5,
                                        bd=0)
        self.viewItemsBtn = tk.Button(self.viewItemsBorder,
                                      image=self.viewItem,
                                      width=245,
                                      height=440,
                                      bd=0,
                                      relief="flat",
                                      command=self.view_items)

        self.viewOutfitsBorder = tk.Frame(self.lowerButtonCont,
                                          highlightbackground="#BDBDBD",
                                          highlightthickness=5,
                                          bd=0)
        self.viewOutfitsBtn = tk.Button(self.viewOutfitsBorder,
                                        image=self.viewOutfit,
                                        width=245,
                                        height=440,
                                        bd=0,
                                        relief="flat",
                                        command=self.view_outfits)

        # error message for the upload of an item
        self.style.configure("UploadError.TFrame", background="#9c9c9c", highlightbackground="#9c9c9c", highlightcolor="#9c9c9c")
        self.uploadErrorFrame = ttk.Frame(self.window, style="UploadError.TFrame")
        self.style.configure("UploadError.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.uploadError = ttk.Label(self.uploadErrorFrame, text="Unsupported file type for upload", style="UploadError.TLabel")
        self.uploadError.pack()

        self.generateOutfitsBtn.pack()
        self.viewItemsBtn.pack()
        self.viewOutfitsBtn.pack()

        self.uploadItemsBorder.pack()
        self.viewItemsBorder.pack(side="left", padx=3)
        self.viewOutfitsBorder.pack(side="right",padx=3)

        self.upperButtonCont.pack()
        self.lowerButtonCont.pack(pady=10)

    def upload_items_from_dir(self):
        self.uploadErrorFrame.place_forget()
        filepath = filedialog.askopenfilename(initialdir="This PC")
        if filepath:
            # checks if the file uploaded is an image that the image removal library can work with
            if filepath.lower().endswith((".png", ".gif", ".jpg", ".jpeg", ".jfif", ".webp", ".tiff", ".bmp")):
                with open("app-text-files/image_paths.txt", "w") as file:
                    file.write(filepath)
                if self.upload_item_window is not None:
                    self.upload_item_window.window.destroy()
                    self.upload_info()
                else:
                    self.upload_info()
            else:
                self.uploadErrorFrame.place(x=0, y=0, relwidth=1)

    def upload_info(self):
        with open("app-text-files/image_paths.txt", "r") as f:
            path = f.readline()
            if len(path) != 0:
                self.upload_item_window = UploadInfo.Popup(self.window, path)

    def view_items(self):
        if self.view_item_window is not None:
            self.view_item_window.window.destroy()
            self.view_item_window = itemview.ViewUserItems(self.parent)
        else:
            self.view_item_window = itemview.ViewUserItems(self.parent)

    def view_outfits(self):
        if self.view_outfit_window is not None:
            self.view_outfit_window.window.destroy()
            self.view_outfit_window = outfitview.ViewOutfits(self.parent)
        else:
            self.view_outfit_window = outfitview.ViewOutfits(self.parent)
