import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3


class HomeScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent

        # initiate images
        self.logo = tk.Canvas(parent, width=160, height=90, background='#f9fdf7', highlightbackground="#f9fdf7")
        self.logo_image = self.get_logo()
        self.logo.create_image(82, 45, image=self.logo_image)

        # initiate frames
        self.navigation = tk.Frame(parent, width=600, height=150, background="#f9fdf7")
        self.outfitHeadingCont = tk.Frame(parent, width=600, height=150, background="#f9fdf7")

        # initiate navigation buttons
        self.homeBtn = tk.Button(self.navigation, background="#f9fdf7", borderwidth=0)
        self.homeBtnImg = tk.PhotoImage(file="HomeBtnImg.png")
        self.homeBtn.config(image=self.homeBtnImg)

        self.generateBtn = tk.Button(self.navigation,
                                     background="#f9fdf7",
                                     borderwidth=0,
                                     command=self.close_and_open_generate)
        self.generateBtnImg = tk.PhotoImage(file="GenerateBtnImg.png")
        self.generateBtn.config(image=self.generateBtnImg)

        self.wardrobeBtn = tk.Button(self.navigation,
                                     background="#f9fdf7",
                                     borderwidth=0,
                                     command=self.close_and_open_wardrobe)
        self.wardrobeBtnImg = tk.PhotoImage(file="WardrobeBtnImg.png")
        self.wardrobeBtn.config(image=self.wardrobeBtnImg)

        self.settingsBtn = tk.Button(self.navigation,
                                     background="#f9fdf7",
                                     borderwidth=0,
                                     command=self.close_and_open_settings)
        self.settingsBtnImg = tk.PhotoImage(file="SettingsBtnImg.png")
        self.settingsBtn.config(image=self.settingsBtnImg)

        # initiate widgets for outfit displays
        self.outfitHeading = ttk.Label(self.outfitHeadingCont,
                                       text="YOUR OUTFITS",
                                       font=("Montserrat Bold", 18),
                                       foreground="#5a6275",
                                       background="#f9fdf7")

        # pack logo and buttons into frames and pack frames onto the app
        self.logo.pack(side=tk.TOP, anchor=tk.NW, pady=3, padx=10)
        self.homeBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.generateBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.wardrobeBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(15, 0))
        self.settingsBtn.pack(side=tk.LEFT,anchor=tk.W, padx=(10, 0))
        self.navigation.pack(pady=(10, 0))

        # pack widgets for displaying outfits
        self.outfitHeading.pack(side=tk.LEFT, anchor=tk.NW)
        self.outfitHeadingCont.pack(pady=(15, 0), padx=(10, 380))

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((160, 90)))
        return resized_image

    # function to close window and open generation menu
    def close_and_open_generate(self):
        self.parent.destroy()
        try:
            import Generate
        except Exception as e:
            print(f"Error: {e}")

    # function to close window and open generation menu
    def close_and_open_wardrobe(self):
        self.parent.destroy()
        try:
            import Wardrobe
        except Exception as e:
            print(f"Error: {e}")

    # function to close window and open generation menu
    def close_and_open_settings(self):
        self.parent.destroy()
        try:
            import Settings
        except Exception as e:
            print(f"Error: {e}")


win = tk.Tk()
win.title("OutfitGenie")
win.geometry("600x800+1000+300")
win.configure(background="#f9fdf7")
HomeScreen(win).pack(expand=True)

win.mainloop()