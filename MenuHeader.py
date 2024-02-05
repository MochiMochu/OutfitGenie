import tkinter as tk
from PIL import Image, ImageTk


class MenuHeader(tk.Frame):
    def __init__(self, parent, window, menu_type, colour_scheme, open_home, open_generate, open_wardrobe, open_settings, *args,
                 **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.window = window
        self.menu_type = menu_type
        self.colour_scheme = colour_scheme
        self.close_and_open_home = open_home
        self.close_and_open_generate = open_generate
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_settings = open_settings

        # initiate images
        self.logo = tk.Canvas(self.window, width=160, height=90, background=self.colour_scheme, highlightbackground=self.colour_scheme)
        self.logo_image = self.get_logo()
        self.logo.create_image(82, 45, image=self.logo_image)

        # initiate frame for navigation buttons
        self.navigation = tk.Frame(self.window, width=600, height=150, background=self.colour_scheme)

        # initiate navigation buttons
        if menu_type != "Home":
            self.homeBtn = tk.Button(self.navigation,
                                     background=self.colour_scheme,
                                     borderwidth=0,
                                     command=self.close_and_open_home)
            self.homeBtnImg = tk.PhotoImage(file="app-images/HomeBtnImg.png")
            self.homeBtn.config(image=self.homeBtnImg)
        else:
            self.homeBtn = tk.Button(self.navigation,
                                     background=self.colour_scheme,
                                     borderwidth=0)
            self.homeBtnImg = tk.PhotoImage(file="app-images/HomeBtnImg.png")
            self.homeBtn.config(image=self.homeBtnImg)

        if menu_type != "Generate":
            self.generateBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0,
                                         command=self.close_and_open_generate)
            self.generateBtnImg = tk.PhotoImage(file="app-images/GenerateBtnImg.png")
            self.generateBtn.config(image=self.generateBtnImg)
        else:
            self.generateBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0)
            self.generateBtnImg = tk.PhotoImage(file="app-images/GenerateBtnImg.png")
            self.generateBtn.config(image=self.generateBtnImg)

        if menu_type != "Wardrobe":
            self.wardrobeBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0,
                                         command = self.close_and_open_wardrobe)
            self.wardrobeBtnImg = tk.PhotoImage(file="app-images/WardrobeBtnImg.png")
            self.wardrobeBtn.config(image=self.wardrobeBtnImg)
        else:
            self.wardrobeBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0)
            self.wardrobeBtnImg = tk.PhotoImage(file="app-images/WardrobeBtnImg.png")
            self.wardrobeBtn.config(image=self.wardrobeBtnImg)

        if menu_type != "Settings":
            self.settingsBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0,
                                         command=self.close_and_open_settings)
            self.settingsBtnImg = tk.PhotoImage(file="app-images/SettingsBtnImg.png")
            self.settingsBtn.config(image=self.settingsBtnImg)
        else:
            self.settingsBtn = tk.Button(self.navigation,
                                         background=self.colour_scheme,
                                         borderwidth=0)
            self.settingsBtnImg = tk.PhotoImage(file="app-images/SettingsBtnImg.png")
            self.settingsBtn.config(image=self.settingsBtnImg)

        # pack logo and navigation buttons into frames and pack frames onto the app
        self.logo.pack(side=tk.TOP, anchor=tk.NW, pady=3, padx=10)
        self.homeBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.generateBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.wardrobeBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(15, 0))
        self.settingsBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(10, 0))
        self.navigation.pack(pady=(10, 0))

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("app-images/AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((160, 90)))
        return resized_image
