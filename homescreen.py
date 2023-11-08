import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import shutil
import os

# clearing previously added images of outfits
directory_path = "C:/Users/jasmi/PycharmProjects/OutfitGenie/outfit-images/"

# List all files and subdirectories in the directory
contents = os.listdir(directory_path)

# Remove each item within the directory
for item in contents:
    item_path = os.path.join(directory_path, item)
    if os.path.isfile(item_path):
        os.remove(item_path)  # Remove files
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)  # Remove subdirectories and their contents


class HomeScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent

        # initiating the database calls
        conn = sqlite3.connect("user_information.db")
        self.c = conn.cursor()

        # initiate images
        self.logo = tk.Canvas(parent, width=160, height=90, background='#f9fdf7', highlightbackground="#f9fdf7")
        self.logo_image = self.get_logo()
        self.logo.create_image(82, 45, image=self.logo_image)
        self.newOutfit = tk.PhotoImage(file="NewOutfit.png")

        # initiate frames
        self.navigation = tk.Frame(parent, width=600, height=150, background="#f9fdf7")
        self.outfitHeadingCont = tk.Frame(parent, width=600, height=150, background="#f9fdf7")
        self.carouselCont = tk.Frame(parent, height=250)
        self.carouselCanvas = tk.Canvas(self.carouselCont, height=260, background='#f9fdf7', highlightthickness=0)
        self.buttonsCont = ttk.Frame(self.carouselCanvas)

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
        # widgets for carousel of buttons
        self.scrollbar = ttk.Scrollbar(self.carouselCont,
                                       orient="horizontal",
                                       command=self.carouselCanvas.xview)
        self.generateOutfitsBtnBorder = tk.Frame(self.buttonsCont,
                                                 highlightbackground="#BDBDBD",
                                                 highlightthickness=3,
                                                 bd=0)
        self.generateOutfitsBtn = tk.Button(self.generateOutfitsBtnBorder,
                                            image=self.newOutfit,
                                            width=150,
                                            height=250,
                                            bd=0,
                                            relief="flat",
                                            command=self.close_and_open_generate)

        # binding view area of the buttons
        self.buttonsCont.bind("<Configure>",
                              lambda e: self.carouselCanvas.configure(
                                  scrollregion=self.carouselCanvas.bbox("all")))

        # create viewing window in the canvas
        self.carouselCanvas.create_window((0, 0), window=self.buttonsCont, anchor="nw")
        self.carouselCanvas.configure(xscrollcommand=self.scrollbar.set)

        # pack logo and buttons into frames and pack frames onto the app
        self.logo.pack(side=tk.TOP, anchor=tk.NW, pady=3, padx=10)
        self.homeBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.generateBtn.pack(side=tk.LEFT, anchor=tk.W)
        self.wardrobeBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(15, 0))
        self.settingsBtn.pack(side=tk.LEFT, anchor=tk.W, padx=(10, 0))
        self.navigation.pack(pady=(10, 0))

        # pack widgets for displaying outfits
        self.outfitHeading.pack(side=tk.LEFT, anchor=tk.NW)
        self.outfitHeadingCont.pack(pady=(15, 0), padx=(10, 380))
        self.carouselCont.pack(fill="x", padx=30, pady=10)
        self.scrollbar.pack(side="bottom", fill="x")
        self.carouselCanvas.pack(side="left", fill="both", expand=True)

        # checking for outfits
        self.outfitsAvailable = self.check_outfits()
        self.load_images()

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((160, 90)))
        return resized_image

    # function to close window and open generation menu
    def close_and_open_generate(self):
        self.c.close()
        self.parent.destroy()
        try:
            import Generate
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

    # get id of user to load any saved outfits
    def get_user_id(self):
        with open("current_user.txt") as f:
            username = f.readline()
        select_query = "select user_id from logins where username = ?"
        self.c.execute(select_query, (username,))
        contents = self.c.fetchall()
        user_id = []
        for item in contents:
            for value in item:
                user_id.append(value)
        return user_id

    # check if any outfits exist
    def check_outfits(self):
        u = self.get_user_id()
        username = u[0]
        print(username)
        select_query = "select outfit_id from outfits where user_id = ?"
        self.c.execute(select_query, (username,))
        answer = self.c.fetchall()
        print(answer)
        items = len(answer)
        login_details = []
        for item in answer:
            for value in item:
                login_details.append(value)
        if items == 0:
            print("no outfits found")
            self.display_empty()
        else:
            self.display_carousel()
        return items

    # loads images of the outfits from the database
    def load_images(self):
        u = self.get_user_id()
        user = u[0]
        fetch_image_query = """SELECT image from clothingItems where user_id = ?"""
        self.c.execute(fetch_image_query, (user,))
        record = self.c.fetchall()
        for index, row in enumerate(record):
            photoPath = "C:/Users/jasmi/PycharmProjects/OutfitGenie/outfit-images/outfit{}.png".format(index)

            with open(photoPath, 'wb') as file:
                file.write(row[0])  # Access the first element of the tuple (the image data)

    # displaying outfits if there are outfits saved
    def display_carousel(self):
        print("displaying buttons")

    # displaying a suggestion to open generate menu if there are currently no outfits saved
    def display_empty(self):
        # packs the widgets to show the button and its border
        self.generateOutfitsBtnBorder.pack()
        self.generateOutfitsBtn.pack()


win = tk.Tk()
win.title("OutfitGenie")
win.geometry("600x800+1000+300")
win.configure(background="#f9fdf7")
HomeScreen(win).pack(expand=True)

win.mainloop()
