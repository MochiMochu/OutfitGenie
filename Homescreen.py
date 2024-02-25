import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import shutil
import os
import requests
from io import BytesIO
import MenuHeader as header
import CentreWindow as cw


class HomeScreen(tk.Frame):
    def __init__(self, parent, open_home, open_generate, open_wardrobe, open_settings, close_app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None
        self.new_outfit = tk.PhotoImage(file="app-images/NewOutfit.png")

        # variables for opening new windows
        self.close_and_open_home = open_home
        self.close_and_open_generate = open_generate
        self.close_and_open_settings = open_settings
        self.close_and_open_wardrobe = open_wardrobe
        self.close_app = close_app

        # initiating the variables for easy database operations
        conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = conn.cursor()

        # initiating instance variables for the Tkinter widgets
        self.outfitHeadingCont = None
        self.carouselCont = None
        self.carouselCanvas = None
        self.buttonsCont = None
        self.outfitHeading = None
        self.scrollbar = None
        self.generateOutfitsBtnBorder = None
        self.generateOutfitsBtn = None
        self.outfitsAvailable = None
        self.carouselButton = None
        self.weatherCont = None
        self.weatherHeaderFrame = None
        self.weatherIconFrame = None
        self.weatherTempFrame = None
        self.weatherHeader = None
        self.locationHeader = None
        self.weatherIcon = None
        self.weatherLabel = None
        self.displayTemp = None
        self.weatherSummary = None
        self.maxTemp = None
        self.minTemp = None
        self.realFeel = None
        self.weatherFetchError = None

        # initiating variables for holding weather information from the API call
        self.place = None
        self.icon = None
        self.current_temp = None
        self.weather_desc = None
        self.high_temp = None
        self.low_temp = None
        self.feels_like = None

        # variable for holding all images in use
        self.outfit_images = []

        # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 800)
        self.window.withdraw()
        self.window.protocol ("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#f9fdf7")
        self.create_widgets()
        self.window.deiconify()

    # fetches the variables necessary to display the weather forecast for the user's area
    def get_weather_variables(self):
        self.api_key = "45303768bf0f4c00898183710231211"
        self.latitude = self.get_latitude()
        self.longitude = self.get_longitude()
        self.weather_url = "http://api.weatherapi.com/v1/forecast.json?q=" + str(self.latitude[0]) + "%20" + str(
            self.longitude[0]) + "&days=1&key=" + self.api_key  # url to be used to fetch the weather data

    def create_widgets(self):
        # initiate frames for carousel and its buttons
        self.outfitHeadingCont = tk.Frame(self.window, width=600, height=150, background="#f9fdf7")
        self.carouselCont = tk.Frame(self.window, height=250)
        self.carouselCanvas = tk.Canvas(self.carouselCont, height=260, background='#f9fdf7', highlightthickness=0)
        self.buttonsCont = ttk.Frame(self.carouselCanvas)

        # initiate widgets for outfit displays
        self.outfitHeading = ttk.Label(self.outfitHeadingCont,
                                       text="YOUR OUTFITS",
                                       font=("Montserrat Bold", 18),
                                       foreground="#5a6275",
                                       background="#f9fdf7")        # heading to label carousel for outfits
        self.scrollbar = ttk.Scrollbar(self.carouselCont,
                                       orient="horizontal",
                                       command=self.carouselCanvas.xview)   # scrollbar to view outfits
        self.generateOutfitsBtnBorder = tk.Frame(self.buttonsCont,
                                                 highlightbackground="#BDBDBD",
                                                 highlightthickness=3,
                                                 bd=0)      # border for the button to recommend generating more outfits
        self.generateOutfitsBtn = tk.Button(self.generateOutfitsBtnBorder,
                                            image=self.new_outfit,
                                            width=150,
                                            height=250,
                                            bd=0,
                                            relief="flat",
                                            command=self.close_and_open_generate)   # button to recommend generating more outfits

        # binding view area of the buttons
        self.buttonsCont.bind("<Configure>",
                              lambda e: self.carouselCanvas.configure(
                                  scrollregion=self.carouselCanvas.bbox("all")))

        # create viewing window in the canvas
        self.carouselCanvas.create_window((0, 0), window=self.buttonsCont, anchor="nw")
        self.carouselCanvas.configure(xscrollcommand=self.scrollbar.set)

        # checking for outfits
        self.outfitsAvailable = self.check_outfits()
        self.load_images()
        self.organise_images()
        if self.outfitsAvailable != 0:
            for i in range(self.outfitsAvailable):
                self.temp_image = tk.PhotoImage(
                    file="outfit-images/cropped-outfit-images/outfit" + str(i) + ".png")
                self.outfit_images.append(self.temp_image)
                if self.temp_image:
                    self.carouselButton = tk.Button(self.buttonsCont,
                                                    image=self.temp_image,
                                                    width=192,
                                                    height=250,
                                                    bd=0,
                                                    relief="flat",
                                                    command=self.close_and_open_generate)
                    self.carouselButton.pack(side="left")
                else:
                    self.display_empty()

        # frames for weather forecast widget
        self.weatherCont = tk.Frame(self.window, width=100, height=360, background="#e0f7ff")
        self.weatherHeaderFrame = tk.Frame(self.weatherCont, width=300, height=120, background="#e0f7ff")
        self.weatherIconFrame = tk.Frame(self.weatherCont, width=300, height=120, background="#e0f7ff")
        self.weatherTempFrame = tk.Frame(self.weatherCont, width=300, height=120, background="#e0f7ff")

        self.weatherFetchError = tk.Label(self.weatherCont,
                                          text="Weather information unavailable at this time.",
                                          font=("Montserrat", 11),
                                          foreground="#5a6275",
                                          background="#e0f7ff")

        self.place, self.icon, self.current_temp, self.weather_desc, self.high_temp, self.low_temp, self.feels_like = self.display_weather()

        # widgets for displaying weather forecast
        self.weatherHeader = tk.Label(self.weatherHeaderFrame,
                                      text="Current weather in",
                                      font=("Montserrat", 15),
                                      foreground="#5a6275",
                                      background="#e0f7ff")
        self.locationHeader = tk.Label(self.weatherHeaderFrame,
                                       text=self.place,
                                       font=("Montserrat", 15),
                                       foreground="#5a6275",
                                       background="#e0f7ff")
        self.weatherIcon = self.load_weather_icon()  # calls function to open the weather icon from the url
        self.weatherLabel = tk.Label(self.weatherIconFrame,
                                     image=self.weatherIcon,
                                     background="#e0f7ff")
        self.displayTemp = tk.Label(self.weatherIconFrame,
                                    text=str(self.current_temp) + "°C",
                                    font=("Book Antiqua", 18),
                                    foreground="#5a6275",
                                    background="#e0f7ff")
        self.weatherSummary = tk.Label(self.weatherIconFrame,
                                       text=self.weather_desc,
                                       font=("Book Antiqua", 15),
                                       foreground="#5a6275",
                                       background="#e0f7ff")
        self.maxTemp = tk.Label(self.weatherTempFrame,
                                text="Highs of " + str(self.high_temp) + "°C",
                                font=("Arial Narrow Italic", 15),
                                foreground="#5a6275",
                                background="#e0f7ff")
        self.minTemp = tk.Label(self.weatherTempFrame,
                                text="Lows of " + str(self.low_temp) + "°C",
                                font=("Arial Narrow Italic", 15),
                                foreground="#5a6275",
                                background="#e0f7ff")
        self.realFeel = tk.Label(self.weatherTempFrame,
                                 text="Feels like "+str(self.feels_like)+"°C",
                                 font=("Arial", 18),
                                 foreground="#5a6275",
                                 background="#e0f7ff")

        # pack widgets for displaying outfits
        self.header = header.MenuHeader(self.parent, self.window, "Home", "#f9fdf7", self.close_and_open_home,
                                        self.close_and_open_generate, self.close_and_open_wardrobe,
                                        self.close_and_open_settings)
        self.outfitHeading.pack(side=tk.LEFT, anchor=tk.NW)
        self.outfitHeadingCont.pack(pady=(15, 0), padx=(10, 380))
        self.carouselCont.pack(fill="x", padx=30, pady=(10, 0))
        self.scrollbar.pack(side="bottom", fill="x")
        self.carouselCanvas.pack(side="left", fill="both", expand=True)

        if not self.place:
            self.weatherFetchError.pack()
            self.weatherCont.pack(padx=(10, 0))
        else:
            # pack widgets for displaying weather
            self.weatherHeader.pack(side=tk.LEFT)
            self.locationHeader.pack(side=tk.LEFT)
            # widgets in the header of the forecast
            self.weatherLabel.place(x=20, y=20)
            self.displayTemp.place(x=120, y=20)
            self.weatherSummary.place(x=120, y=55)
            # icon, temperature and general description of weather for the day
            self.maxTemp.place(x=20, y=10)
            self.minTemp.place(x=160, y=10)
            self.realFeel.place(x=50, y=55)
            # min and max temperature and what it feels like
            self.weatherCont.pack(padx=(10, 0), pady=(15,0))
            self.weatherHeaderFrame.pack()
            self.weatherIconFrame.pack(side=tk.TOP)
            self.weatherTempFrame.pack()

    # get id of user to load any saved outfits
    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id

    # function to get latitude of user's location
    def get_latitude(self):
        user_id = self.get_user_id()
        lat_query = """SELECT Latitude FROM Users WHERE User_ID = ?"""
        self.c.execute(lat_query, (user_id,))
        result = self.c.fetchall()
        latitude = []
        for i in result:
            for value in i:
                latitude.append(value)
        return latitude

    # function to get longitude of user's location
    def get_longitude(self):
        user_id = self.get_user_id()
        lng_query = """SELECT Longitude FROM Users WHERE User_ID = ?"""
        self.c.execute(lng_query, (user_id,))
        result = self.c.fetchall()
        longitude = []
        for i in result:
            for value in i:
                longitude.append(value)
        return longitude

    # check if any outfits exist and cap the number that can be displayed to 5
    def check_outfits(self):
        user_id = self.get_user_id()
        select_query = "SELECT Outfit_ID FROM User_Outfits WHERE User_ID = ?"
        self.c.execute(select_query, (user_id,))
        items = [row[0] for row in self.c.fetchall()]
        num_items = len(items)
        if len(items) == 0:
            self.display_empty()
        elif len(items) >5:
            num_items = 5
        return num_items

    # loads images of the outfits from the database
    def load_images(self):
        user_id = self.get_user_id()  # fetches user id from current user file
        fetch_image_query = """SELECT Outfit_Image FROM User_Outfits WHERE User_ID = ? LIMIT ?"""
        self.c.execute(fetch_image_query, (user_id, self.outfitsAvailable))
        record = self.c.fetchall()
        for file in os.listdir("outfit-images"):
            file_path = os.path.join("outfit-images", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        for index, row in enumerate(record):
            photo_path = "outfit-images/outfit{}.png".format(index)
            with open(photo_path, 'wb') as file:
                file.write(row[0])  # Access the first element of the tuple (the image data)

    # calls function to crop image for every item in the directory
    def organise_images(self):
        num = self.outfitsAvailable
        for file in os.listdir("outfit-images/cropped-outfit-images"):
            file_path = os.path.join("outfit-images/cropped-outfit-images", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        for i in range(num):
            image = Image.open("C:/Users/jasmi/PycharmProjects/OutfitGenie/outfit-images/outfit" + str(i) + ".png")
            newimage = self.crop_image(image)
            savedimage = newimage.save("outfit-images/cropped-outfit-images/outfit" + str(i) + ".png")
            os.remove("outfit-images/outfit" + str(i) + ".png")

    # crops the image around the objects and resizes to fit inside the buttons
    def crop_image(self, image):
        resized_image = image.resize((192, 250))
        return resized_image

    # displaying a suggestion to open generate menu if there are currently no outfits saved
    def display_empty(self):
        # packs the widgets to show the button and its border
        self.generateOutfitsBtnBorder.pack()
        self.generateOutfitsBtn.pack()

    # display weather
    def display_weather(self):
        fetch_success = False
        try:
            fetch = requests.get(self.weather_url)  # using python requests package to access the url
            response = fetch.json() # fetches the json response
            fetch_success = True
        except:
            self.weatherFetchError.pack()

        if fetch_success:
            # accesses the necessary aspects of the json file and sets them as temp variables to be returned
            location = response["location"]["name"]
            icon = response["current"]["condition"]["icon"]
            current_temp = response["current"]["temp_c"]
            dayDesc = response["forecast"]["forecastday"][0]["day"]["condition"]["text"]
            high_temp = response["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
            low_temp = response["forecast"]["forecastday"][0]["day"]["mintemp_c"]
            feels_like = response["current"]["feelslike_c"]
            return location, icon, current_temp, dayDesc, high_temp, low_temp, feels_like
        else:

            return None, None, None, None, None, None, None

    # loads the weather icon from the given url
    def load_weather_icon(self):
        icon_fetch_success = False
        if self.icon:
            url = "https:" + self.icon  # accesses the url of the image file
            try:
                response = requests.get(url)
                image_data = response.content
                icon_fetch_success = True
            except:
                return None
            if icon_fetch_success:
                image = Image.open(BytesIO(image_data))  # opens the image to be used
                return ImageTk.PhotoImage(image)

