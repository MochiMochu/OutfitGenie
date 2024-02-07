import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk, ImageChops
import MenuHeader as header
import requests
import datetime
import io
import CentreWindow as cw


class GenerateMenu(tk.Frame):
    def __init__(self, parent, open_home, open_generate, open_wardrobe, open_settings, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None
        self.ErrorStyle = ttk.Style()
        self.ErrorFrameStyle = ttk.Style()
        self.clothing_categories = {"t-shirt": "top",
                                    "graphic tee": "top",
                                    "polo shirt": "top",
                                    "corset": "top",
                                    "off the shoulder top": "top",
                                    "bodysuit": "top",
                                    "camisole": "top",
                                    "crop top": "top",
                                    "tube top": "top",
                                    "tank top": "top",
                                    "formal shirt": "top",
                                    "blouse": "top",
                                    "turtleneck": "top",
                                    "jumper": "top",
                                    "cardigan": "outerwear",
                                    "sweatshirt": "outerwear",
                                    "hoodie": "outerwear",
                                    "joggers": "bottom",
                                    "jeans": "bottom",
                                    "cargo pants": "bottom",
                                    "flares": "bottom",
                                    "leggings": "bottom",
                                    "slacks": "bottom",
                                    "suit pants": "bottom",
                                    "hot pants": "bottom",
                                    "bermuda shorts": "bottom",
                                    "shorts": "bottom",
                                    "mini skirt": "bottom",
                                    "midi skirt": "bottom",
                                    "maxi skirt": "bottom",
                                    "mini dress": "onepiece",
                                    "midi dress": "onepiece",
                                    "maxi dress": "onepiece",
                                    "bodycon dress": "onepiece",
                                    "dungarees": "onepiece",
                                    "jumpsuit": "onepiece",
                                    "overalls": "onepiece",
                                    "blazer": "outerwear",
                                    "gilet": "outerwear",
                                    "fur coat": "outerwear",
                                    "puffer coat": "outerwear",
                                    "jacket": "outerwear",
                                    "parka": "outerwear",
                                    "trench coat": "outerwear"
                                }

        # variables for opening new windows
        self.close_and_open_home = open_home
        self.close_and_open_settings = open_settings
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_generate = open_generate
        self.close_app = close_app

        # initiating the database calls
        conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = conn.cursor()

        # initiating instance variables to be modified later
        self.button = None
        self.occasionStyle = None
        self.occasionList = None
        self.sortedOccasions = None
        self.occasion = None
        self.chooseOccasion = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 800)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#dcf5df")
        self.create_generate_widgets()
        self.header = header.MenuHeader(self.parent, self.window, "Generate", "#dcf5df", self.close_and_open_home,
                                        self.close_and_open_generate, self.close_and_open_wardrobe,
                                        self.close_and_open_settings)
        self.header.pack()

    def create_generate_widgets(self):
        # button for generating a new outfit
        self.buttonImg = tk.PhotoImage(file="app-images/button.png")
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

        # error message if there aren't enough clothing items to be able to generate an outfit
        self.ErrorInsufficientFrame = ttk.Frame(self.window, style = "Error.TFrame")
        self.insufficientError = ttk.Label(self.ErrorInsufficientFrame, text="Insufficient items uploaded", style="Error.TLabel")
        self.insufficientError.pack()

    # function to get list of occasions
    def get_occasions(self):
        self.c.execute("""SELECT Occasion_Name FROM Occasions""")
        response = self.c.fetchall()
        occasions = []
        for item in response:
            for value in item:
                occasions.append(value)
        return occasions

    # fetches the variables necessary to display the weather forecast for the user's area
    def get_weather(self):
        api_key = "45303768bf0f4c00898183710231211"
        latitude = self.get_latitude()
        longitude = self.get_longitude()
        weather_url = "http://api.weatherapi.com/v1/forecast.json?q=" + str(latitude) + "%20" + str(
            longitude) + "&days=1&key=" + api_key  # url to be used to fetch the weather data
        fetch = requests.get(weather_url)
        response = fetch.json()  # fetches the json response
        feels_like = response["current"]["feelslike_c"]

        return feels_like

    # sorting occasions in alphabetical order using merge sort
    def sort_occasions(self, occasions):
        occasion = sorted(occasions)
        return occasions

    # displays error message that the number of items uploaded is not enough for an outfit to be generated
    def error_not_sufficient(self):
        self.ErrorInsufficientFrame.place(x=0, y=770, relwidth=1)

    def create_outfits(self):
        occasion = self.occasion.get()
        if occasion == "Select Occasion":
            self.ErrorFrame.place(x=0, y=770, relwidth=1)
        else:
            occasion = self.occasion.get()
            self.ErrorFrame.place_forget()
            feels_like = int(self.get_weather())
            possible_items = self.retrieve_occasion_and_user_items(occasion)  # fetches ID of all user items that are appropriate for the occasion
            if not possible_items:
                self.error_not_sufficient()
            else:
                tops, bottoms, onepieces, outerwear = self.sort_items(possible_items)  # sorts IDs into categories of clothing
                check_sufficient = self.check_enough_items(tops, bottoms)
                if not check_sufficient:
                    self.error_not_sufficient()
                else:
                    thickness, outerwear_needed, bottoms_type = self.requirements_by_temperature(feels_like)

    # sorts the IDs into separate lists for what type of clothing they are (tops, bottoms, outerwear or onepieces)
    def sort_items(self, possible_items):
        type_query = """SELECT Clothing_Type FROM Clothing_Items WHERE Item_ID = ?"""
        for id in possible_items:
            self.c.execute(type_query, (id,))
        response = self.c.fetchall()
        all_types = []
        for count in response:
            for type in count:
                all_types.append(type)
        # convert the type of clothing into the category (bottom, top, onepiece or outerwear)
        for i in range (len(all_types)):
            all_types[i] = self.clothing_categories[all_types[i].lower()]

        # split the item IDs into lists depending on their category
        tops = []
        bottoms = []
        onepieces = []
        outerwear = []
        for j in range(len(all_types)):
            if all_types[j] == "bottom":
                bottoms.append(possible_items[j])
            elif all_types[j] == "top":
                tops.append(possible_items[j])
            elif all_types[j] == "onepiece":
                onepieces.append(possible_items[j])
            else:
                outerwear.append(possible_items[j])
        return tops, bottoms, onepieces, outerwear

    # filters down the list of IDs based on the current real feel temperature
    def requirements_by_temperature(self, feels_like):
        thickness = ""
        outerwear_needed = ""
        bottoms_type = ""
        if feels_like <= 13:
            thickness = "thick"
            outerwear_needed = "coats"
            bottoms_type = "long"
        elif 13 < feels_like <= 20:
            thickness = "medium"
            outerwear_needed = "either"
            bottoms_type = "long"
        elif 20 < feels_like <= 25:
            thickness = "thin"
            outerwear_needed = "jumper"
            bottom_types = "short"
        else:
            thickness = "thin"
            outerwear_needed = "none"
            bottoms_type = "short"
        return thickness, outerwear_needed, bottoms_type

    # checks if there are enough items to generate a basic outfit
    def check_enough_items(self, tops, bottoms):
        # checks if there are any tops or bottoms matching the occasion
        if len(tops) == 0 or len(bottoms) == 0:
            return False
        else:
            check_thickness_query = """SELECT Clothing_Thickness FROM Clothing_Items WHERE Item_ID = ?"""
            # checking if there is at least one item of each thickness in the top and bottoms section for minimum outfit generation
            top_thickness_check = []
            for item in tops:
                self.c.execute(check_thickness_query, (item, ))
            response = self.c.fetchall()
            for i in range(len(response[0])):
                top_thickness_check.append(response[0][i])
            top_thickness_check = list(dict.fromkeys(top_thickness_check))
            variants = 0
            for value in top_thickness_check:
                if value.lower() == "thick" or value.lower() == "medium" or value.lower() == "thin":
                    variants += 1
            if variants != 3:
                return False
            else:
                bottom_thickness_check = []
                for item in bottoms:
                    self.c.execute(check_thickness_query, (item,))
                response = self.c.fetchall()
                for i in range(len(response[0])):
                    bottom_thickness_check.append(response[0][i])
                bottom_thickness_check = list(dict.fromkeys(bottom_thickness_check))
                variants = 0
                for value in bottom_thickness_check:
                    if value.lower() == "thick" or value.lower() == "medium" or value.lower() == "thin":
                        variants += 1
                if variants != 3:
                    return False
                else:
                    # checking if there is at least one item of each bottom length for minimum outfit generation
                    long_bottoms = ["joggers", "jeans", "cargo pants", "flares", "leggings", "slacks", "suit pants",
                                    "dungarees", "jumpsuit", "overalls"]
                    short_bottoms = ["hot pants", "shorts", "bermuda shorts", "mini skirt", "midi skirt", "bodycon dress",
                                     "mini dress"]
                    num_long = 0
                    num_short = 0
                    check_bottom_length_query = """SELECT Clothing_Type FROM Clothing_Items where Item_ID = ?"""
                    for item in bottoms:
                        self.c.execute(check_bottom_length_query, (item, ))
                    response = self.c.fetchall()
                    for record in response:
                        for entry in record:
                            if entry.lower() in long_bottoms:
                                num_long += 1
                            else:
                                num_short += 1
                    if num_short < 1 or num_long < 1:
                        return False
                    else:
                        return True

    def filter_by_colour(self, possible_items):
        colour_query = """SELECT Primary_Colour FROM Clothing_Items WHERE Item_ID = ?"""
        for item in possible_items:
            self.c.execute(colour_query, (item,))
        response = self.c.fetchall()
        duplicate_colours = []
        for count in response:
            for item in count:
                duplicate_colours.append(item)

        # removing duplicates in the list
        all_colours = list(dict.fromkeys(duplicate_colours))

    # function to get latitude of user's location
    def get_latitude(self):
        user_id = self.get_user_id()
        lat_query = """SELECT Latitude from Users WHERE User_ID = ?"""
        self.c.execute(lat_query, (user_id,))
        result = self.c.fetchall()
        latitude = result[0][0]
        return latitude

    # function to get longitude of user's location
    def get_longitude(self):
        user_id = self.get_user_id()
        lng_query = """SELECT Longitude from Users WHERE User_ID = ?"""
        self.c.execute(lng_query, (user_id,))
        result = self.c.fetchall()
        longitude = result[0][0]
        return longitude

    # get id of user to load any saved outfits
    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id

    # get the occasion
    def retrieve_occasion_id(self, occasion):
        occasion_id_query = """SELECT Occasion_ID FROM Occasions WHERE Occasion_Name = ?"""
        self.c.execute(occasion_id_query, (occasion,))
        response = self.c.fetchall()
        occasion_id = response[0][0]
        return occasion_id

    def retrieve_user_items(self):
        user_id = self.get_user_id()
        occasion_item_query = """SELECT Item_ID FROM Clothing_Items WHERE User_ID = ?"""
        self.c.execute(occasion_item_query, (user_id,))
        response = self.c.fetchall()
        all_items = []
        for item in response:
            for value in item:
                all_items.append(value)
        return all_items

    def retrieve_occasion_and_user_items(self, occasion):
        occasion_id = self.retrieve_occasion_id(occasion)
        all_items = self.retrieve_user_items()
        available_items = []
        for item in all_items:
            occasion_and_user_query = """SELECT Item_ID FROM Items_Occasions WHERE Item_ID = ? AND Occasion_ID = ?"""
            self.c.execute(occasion_and_user_query, (item, occasion_id))
            response = self.c.fetchall()
            if response:
                available_items.append(response[0][0])
        return available_items

    # returns the images of the items that were chosen to be in the outfit
    def retrieve_selected_images(self, item_ids):
        image_query = """SELECT Clothing_Image FROM Clothing_Items WHERE Item_ID = ?"""
        num = 0
        # fetches each of the BLOBs for the item_IDs and saves them to a temporary folder
        for item in item_ids:
            num += 1
            self.c.execute(image_query, (item,))
            response = self.c.fetchall()
            blob_img = response[0][0]
            img = Image.open(io.BytesIO(blob_img))
            img.save("C:/Users/jasmi/PycharmProjects/OutfitGenie/temp-item-images/item" + str(num) + ".png")

    # item IDs have to be passed in the order: top, bottoms, outerwear
    def compile_images(self, item_ids):
        item_x_coords =[35, 35, 250]  # x coordinates for where the top left corner of the image will be (different for each item)
        item_y_coords = [5, 280, 40]  # the same but for the y coordinates
        num_items = len(item_ids)
        background = Image.open("app-images/white_bg.png")  # standard white background to place the item images on
        resized_bg = background.resize((500, 650))  # resizes the background to display

        # loops through the items and places them on the white background according to the coordinates above
        for i in range(num_items):
            overlay_image = self.resize_image("item"+str(i)+".png")
            resized_bg.paste(overlay_image, (item_x_coords[i], item_y_coords[i]), overlay_image)
            resized_bg.save("C:/Users/jasmi/PycharmProjects/OutfitGenie/temp-outfit-images/newoutfit")

    # resizes the image to fit the background according to its original aspect ratio
    def resize_image(self, image_path):
        overlay_image = Image.open(image_path)
        original_width = overlay_image.size[0]
        scale = (250 / float(original_width))
        height = int((float(overlay_image.size[1]) * float(scale)))
        resized_overlay = overlay_image.resize((250, height))

        return resized_overlay


# notes for working on this tomorrow: need to clear the temp-outfit and temp-item folder before generating new item
# also save the outfit to the database and to the outfit-images folder so it displays on the homescreen






