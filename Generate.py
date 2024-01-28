import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk, ImageChops
import tkinter.font as tkFont


class GenerateMenu(tk.Frame):
    def __init__(self, parent, open_home, open_settings, open_wardrobe, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None
        self.ErrorStyle = ttk.Style()
        self.ErrorFrameStyle = ttk.Style()

        # variables for opening new windows
        self.close_and_open_home = open_home
        self.close_and_open_settings = open_settings
        self.close_and_open_wardrobe = open_wardrobe
        self.close_app = close_app

        # initiating the database calls
        conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = conn.cursor()

        # initiating instance variables to be modified later
        self.logo = None
        self.logo_image = None
        self.newOutfit = None
        self.navigation = None
        self.homeBtn = None
        self.homeBtnImg = None
        self.generateBtn = None
        self.generateBtnImg = None
        self.wardrobeBtn = None
        self.wardrobeBtnImg = None
        self.settingsBtn = None
        self.settingsBtnImg = None
        self.buttonImg = None
        self.button = None
        self.occasionStyle = None
        self.occasionList = None
        self.sortedOccasions = None
        self.occasion = None
        self.chooseOccasion = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#dcf5df")
        self.window.geometry("600x800+1000+300")
        self.create_widgets()

    def create_widgets(self):
        # initiate images
        self.logo = tk.Canvas(self.window, width=160, height=90, background='#dcf5df', highlightbackground="#dcf5df")
        self.logo_image = self.get_logo()
        self.logo.create_image(82, 45, image=self.logo_image)
        self.newOutfit = tk.PhotoImage(file="NewOutfit.png")

        # initiate frame for navigation buttons
        self.navigation = tk.Frame(self.window, width=600, height=150, background="#dcf5df")

        # initiate navigation buttons
        self.homeBtn = tk.Button(self.navigation,
                                 background="#dcf5df",
                                 borderwidth=0,
                                 command=self.close_and_open_home)
        self.homeBtnImg = tk.PhotoImage(file="HomeBtnImg.png")
        self.homeBtn.config(image=self.homeBtnImg)

        self.generateBtn = tk.Button(self.navigation,
                                     background="#dcf5df",
                                     borderwidth=0)
        self.generateBtnImg = tk.PhotoImage(file="GenerateBtnImg.png")
        self.generateBtn.config(image=self.generateBtnImg)

        self.wardrobeBtn = tk.Button(self.navigation,
                                     background="#dcf5df",
                                     borderwidth=0,
                                     command=self.close_and_open_wardrobe)
        self.wardrobeBtnImg = tk.PhotoImage(file="WardrobeBtnImg.png")
        self.wardrobeBtn.config(image=self.wardrobeBtnImg)

        self.settingsBtn = tk.Button(self.navigation,
                                     background="#dcf5df",
                                     borderwidth=0,
                                     command=self.close_and_open_settings)
        self.settingsBtnImg = tk.PhotoImage(file="SettingsBtnImg.png")
        self.settingsBtn.config(image=self.settingsBtnImg)

        # pack logo and navigation buttons into frames and pack frames onto the app
        self.logo.pack(side=tk.TOP, anchor=tk.NW, pady=3, padx=10)
        self.homeBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.generateBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.wardrobeBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(15, 0))
        self.settingsBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(10, 0))
        self.navigation.pack(pady=(10, 0))

        # button for generating a new outfit
        self.buttonImg = tk.PhotoImage(file="button.png")
        self.button = tk.Button(self.window,
                                background="#dcf5df",
                                borderwidth=0,
                                command=self.create_outfits)
        self.button.config(image=self.buttonImg)
        self.button.place(x=140, y=200)

        # drop down menu to select the occasion for consideration by the generation algorithm
        self.occasionStyle = ttk.Style()
        self.occasionStyle.configure("occasion.TMenubutton",
                                     font=("Arial", 20))  # sets the style for the drop down menu
        self.occasionList = self.get_occasions()  # fetches the list of occasions in the database
        self.sortedOccasions = self.sort_occasions(self.occasionList)  # sorts the occasions using a merge sort
        self.occasion = tk.StringVar(self.window)  # variable for storing the user's response in the occasion drop down
        self.occasion.set("Select Occasion")  # sets the default text of the menu to be "Select Occasion"
        self.chooseOccasion = ttk.OptionMenu(self.window, self.occasion, self.occasion.get(), *self.occasionList,
                                             style="occasion.TMenubutton")
        self.chooseOccasion.config(width=30)
        self.chooseOccasion.place(x=60, y=550)

        # error message if an occasion hasn't been chosen and the generate button is clicked
        self.ErrorFrameStyle.configure("Error.TFrame",
                                  background="#9c9c9c",
                                  highlightbackground="#9c9c9c",
                                  hightlightcolor="#9c9c9c")
        self.ErrorStyle.configure("Error.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.ErrorFrame = ttk.Frame(self.window, style = "Error.TFrame")
        self.occasionError = ttk.Label(self.ErrorFrame, text="Please select an occasion", style="Error.TLabel" )
        self.occasionError.pack()

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((160, 90)))
        return resized_image

    # function to get list of occasions
    def get_occasions(self):
        self.c.execute("""SELECT Occasion_Name FROM Occasions""")
        response = self.c.fetchall()
        occasions = []
        for item in response:
            for value in item:
                occasions.append(value)
        return occasions

    # sorting occasions in alphabetical order using merge sort
    def sort_occasions(self, occasions):
        if len(occasions) > 1:
            midpoint = len(occasions) // 2
            leftHalf = occasions[midpoint:]
            rightHalf = occasions[:midpoint]
            self.sort_occasions(leftHalf)
            self.sort_occasions(rightHalf)
            i = 0
            j = 0
            k = 0
            while i < len(leftHalf) and j < len(rightHalf):
                if leftHalf[i] < rightHalf[j]:
                    occasions[k] = leftHalf[i]
                    i += 1
                else:
                    occasions[k] = rightHalf[j]
                    j += 1
                k = k + 1
            while i < len(leftHalf):
                occasions[k] = leftHalf[i]
                i = i + 1
                k += 1
            while j < len(rightHalf):
                occasions[k] = rightHalf[j]
                j += 1
                k += 1
        return occasions

    def create_outfits(self):
        occasion = self.occasion.get()
        print(occasion)
        if occasion == "Select Occasion":
            self.ErrorFrame.place(x=0, y=770, relwidth=1)



