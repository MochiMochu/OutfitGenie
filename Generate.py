import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk, ImageChops
import tkinter.font as tkFont

class GenerateMenu(tk.Frame):
    def __init__(self,parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent

        # initiating the database calls
        conn = sqlite3.connect("user_information.db")
        self.c = conn.cursor()

        # initiate images
        self.logo = tk.Canvas(parent, width=160, height=90, background='#dcf5df', highlightbackground="#dcf5df")
        self.logo_image = self.get_logo()
        self.logo.create_image(82, 45, image=self.logo_image)
        self.newOutfit = tk.PhotoImage(file="NewOutfit.png")

        # initiate frame for navigation buttons
        self.navigation = tk.Frame(parent, width=600, height=150, background="#dcf5df")

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
        self.button = tk.Button(parent,
                                background="#dcf5df",
                                borderwidth=0)
        self.button.config(image=self.buttonImg)
        self.button.place(x=140, y=200)

        # drop down menu to select the occasion for consideration by the generation algorithm
        self.occasionStyle = ttk.Style()
        self.occasionStyle.configure("occasion.TMenubutton", font=("Arial", 20))
        self.occasionList = self.get_occasions()
        self.sortedOccasions = self.sort_occasions()
        self.occasion = tk.StringVar(parent)
        self.occasion.set(self.occasionList[0])
        self.chooseOccasion = ttk.OptionMenu(parent, self.occasion, *self.sortedOccasions, style="occasion.TMenubutton")
        self.chooseOccasion.config(width=30)
        self.chooseOccasion.place(x=60, y=550)

    ### functions from homescreen.py to navigate between menus
    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((160, 90)))
        return resized_image

    # function to close window and open homescreen
    def close_and_open_home(self):
        self.c.close()
        self.parent.destroy()
        try:
            import homescreen
        except Exception as e:
            print(f"Error: {e}")

    # function to close window and open generation menu
    def close_and_open_wardrobe(self):
        self.c.close()
        self.parent.destroy()
        try:
            import Wardrobe
        except Exception as e:
            print(f"Error: {e}")

    # function to close window and open generation menu
    def close_and_open_settings(self):
        self.c.close()
        self.parent.destroy()
        try:
            import Settings
        except Exception as e:
            print(f"Error: {e}")

    # function to get list of occasions
    def get_occasions(self):
        self.c.execute("""SELECT name from Occasions""")
        response = self.c.fetchall()
        occasions = []
        for item in response:
            for value in item:
                occasions.append(value)
        occasions.insert(0, "Select Occasion")
        return occasions

    # sorting occasions in alphabetical order using merge sort
    def sort_occasions(self):
        occasions = self.occasionList
        if len(occasions)>1:
            midpoint=len(occasions)//2
            leftHalf = occasions[midpoint:]
            rightHalf = occasions[:midpoint]
            mergeSort(leftHalf)
            mergeSort(rightHalf)
            i=0
            j=0
            k=0
            while i < len(leftHalf) and j < len(rightHalf):
              if leftHalf[i] < rightHalf[j]:
                occasions[k]=leftHalf[i]
                i+=1
              else:
                occasions[k]=rightHalf[j]
                j+=1
              k=k+1
            while i < len(leftHalf):
              occasions[k]=leftHalf[i]
              i=i+1
              k+=1
            while j < len(rightHalf):
              occasions[k]= rightHalf[j]
              j+=1
              k+=1
        return occasions

win = tk.Tk()
win.title("OutfitGenie")
win.geometry("600x800+1000+300")
win.configure(background="#dcf5df")
GenerateMenu(win).pack(expand=True)

win.mainloop()
