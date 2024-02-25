import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk, ImageChops
import MenuHeader as header
import requests
from datetime import datetime
import io
import CentreWindow as cw
import random
import os
import time
import uuid


class GenerateMenu(tk.Frame):
    def __init__(self, parent, open_home, open_generate, open_wardrobe, open_settings, close_app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.window = None
        self.error_style = ttk.Style()
        self.error_frame_style = ttk.Style()
        self.newoutfit_path = "temp-outfit-images/newoutfit.png"

        # variable to track presence of outfit confirmation popup
        self.outfit_confirmation_window = None

        # reference for image object when displaying generated outfit
        self.generatedOutfit = None

        self.long_bottoms = ["joggers", "jeans", "cargo pants", "flares", "leggings", "slacks", "suit pants",
                             "maxi skirt"]
        self.short_bottoms = ["hot pants", "shorts", "bermuda shorts", "mini skirt", "midi skirt"]

        # variables for opening new windows
        self.close_and_open_home = open_home
        self.close_and_open_settings = open_settings
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_generate = open_generate
        self.close_app = close_app

        # initiating the database calls
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()

        # initiating instance variables for tkinter widgets
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
        self.buttonImg = tk.PhotoImage(file="app-images/GenerateAlgButton.png")
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
        self.error_frame_style.configure("Alert.TFrame",
                                         background="#9c9c9c",
                                         highlightbackground="#9c9c9c",
                                         hightlightcolor="#9c9c9c")
        self.error_style.configure("Alert.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.ErrorFrame = ttk.Frame(self.window, style="Alert.TFrame")
        self.occasionError = ttk.Label(self.ErrorFrame, text="Please select an occasion", style="Alert.TLabel")
        self.occasionError.pack()

        # error message if there aren't enough clothing items to be able to generate an outfit
        self.errorInsufficientFrame = ttk.Frame(self.window, style="Alert.TFrame")
        self.insufficientError = ttk.Label(self.errorInsufficientFrame, text="Insufficient items uploaded",
                                           style="Alert.TLabel")

        # success message if an outfit was generated
        self.successMessageFrame = ttk.Frame(self.window, style="Alert.TFrame")
        self.successCreation = ttk.Label(self.successMessageFrame, text="Outfit saved", style="Alert.TLabel")
        self.successCreation.pack()

        self.insufficientError.pack()

    # function to get list of occasions
    def get_occasions(self):
        self.c.execute("""SELECT Occasion_Name FROM Occasions""")
        occasions = [row[0] for row in self.c.fetchall()]
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
        return occasion

    # displays error message that the number of items uploaded is not enough for an outfit to be generated
    def error_not_sufficient(self):
        self.errorInsufficientFrame.place(x=0, y=770, relwidth=1)

    # calls functions to determine what outfit will be generated 
    def create_outfits(self):
        occasion = self.occasion.get()
        # checks if an occasion was entered by the user
        if occasion == "Select Occasion":
            self.ErrorFrame.place(x=0, y=770, relwidth=1)
        else:
            occasion = self.occasion.get()  # fetches the user-entered occasion from the dropdown box
            occasion_id = self.retrieve_occasion_id(occasion)
            self.ErrorFrame.place_forget()
            feels_like = int(self.get_weather())  # gets what the current temperature feels like
            possible_items = self.retrieve_occasion_and_user_items(
                occasion)  # fetches ID of all user items that are appropriate for the occasion
            # checks if any items exist for the occasion, if not, display an error informing the user that there are too
            # few items
            if not possible_items:
                print("No possible items")
                self.error_not_sufficient()
            else:
                self.errorInsufficientFrame.place_forget()
                tops, bottoms, onepieces, outerwear = self.sort_items(
                    possible_items)  # sorts IDs into categories of clothing
                print("tops and bottoms", tops, bottoms)
                check_sufficient = self.check_enough_items(tops, bottoms)
                if not check_sufficient:
                    print("check sufficient failed")
                    self.error_not_sufficient()
                else:
                    self.errorInsufficientFrame.place_forget()
                    # determines requirements for clothing based on the current temperature
                    thickness, outerwear_needed, bottoms_type = self.requirements_by_temperature(feels_like)
                    chosen_ids = self.filter_by_temperature(thickness, bottoms_type, tops, bottoms, onepieces,
                                                            occasion_id, outerwear_needed)
                    print(chosen_ids)
                    self.call_colour_filtering(chosen_ids, occasion, outerwear_needed, outerwear)
                    # if outerwear_result is None:

    # reduces the list of IDs of the user items to those suitable for the occasion entered
    def retrieve_occasion_and_user_items(self, occasion):
        occasion_id = self.retrieve_occasion_id(occasion)
        all_items = self.retrieve_user_items()
        available_items = []
        # checks each of the user's items - if they match the occasion, they are appended to the list
        for item in all_items:
            occasion_and_user_query = """SELECT Item_ID FROM Clothing_Occasions WHERE Item_ID = ? AND Occasion_ID = ?"""
            self.c.execute(occasion_and_user_query, (item, occasion_id))
            response = self.c.fetchall()
            if response:
                available_items.append(response[0][0])
        print("reduced available items based on occasion", available_items)
        return available_items

    # get the occasion_id from the occasion_name
    def retrieve_occasion_id(self, occasion):
        occasion_id_query = """SELECT Occasion_ID FROM Occasions WHERE Occasion_Name = ?"""
        self.c.execute(occasion_id_query, (occasion,))
        response = self.c.fetchall()
        occasion_id = response[0][0]
        return occasion_id

    # returns the IDs of all the user's items
    def retrieve_user_items(self):
        user_id = self.get_user_id()
        occasion_item_query = """SELECT Item_ID FROM Clothing_Items WHERE User_ID = ?"""
        self.c.execute(occasion_item_query, (user_id,))
        response = self.c.fetchall()
        print(response)
        all_items = []
        for item in response:
            for value in item:
                all_items.append(value)
        print("all_items", all_items)
        return all_items

    # get id of user to load any saved outfits
    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id

    # sorts the IDs into separate lists for what type of clothing they are (tops, bottoms, outerwear or one-pieces)
    def sort_items(self, possible_items):
        # returns the clothing type of every item in the list of occasion suitable items
        all_types = []
        type_query = """SELECT Clothing_Type FROM Clothing_Items WHERE Item_ID = ?"""
        for id in possible_items:
            self.c.execute(type_query, (id,))
            response = self.c.fetchall()
            all_types.append(response[0][0])

        # convert the type of clothing into the level (bottom, top, onepiece or outerwear)
        level_query = """SELECT Level FROM Clothing_Levels WHERE Clothing_Type = ?"""
        for count, type in enumerate(all_types):
            self.c.execute(level_query, (type,))
            result = self.c.fetchall()
            all_types[count] = result[0][0]

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

    # checks if there are enough items to generate a basic outfit
    def check_enough_items(self, tops, bottoms):
        # checks if there are any tops or bottoms matching the occasion
        if len(tops) == 0 or len(bottoms) == 0:
            return False
        else:
            # checks if there are tops and bottoms of each thickness so an outfit appropriate for the weather is generated
            if self.check_thickness(tops):
                print("check top thickness", self.check_thickness(tops))
                if self.check_thickness(bottoms):
                    print("check bottoms thickness", self.check_thickness(bottoms))
                    # checking if there is at least one item of each bottom length for minimum outfit generation
                    num_long = 0
                    num_short = 0
                    check_bottom_length_query = """SELECT Clothing_Type FROM Clothing_Items where Item_ID = ?"""
                    for item in bottoms:
                        self.c.execute(check_bottom_length_query, (item,))
                        response = self.c.fetchall()
                        entry = response[0][0]
                        print(entry)
                        if entry.lower() in self.long_bottoms:
                            num_long += 1
                        else:
                            num_short += 1
                    print("num long", num_long, "num short", num_short)
                    if num_short < 1 or num_long < 1:
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return False

    # function called to check whether there is an item of each thickness in the given set of clothing IDs
    def check_thickness(self, clothing_ids):
        check_thickness_query = """SELECT Clothing_Thickness FROM Clothing_Items WHERE Item_ID = ?"""
        thicknesses = []
        for item in clothing_ids:
            self.c.execute(check_thickness_query, (item,))
            response = self.c.fetchall()
            thicknesses.append(response[0][0])
        # removing duplicates by converting to a dictionary and back
        thicknesses = list(dict.fromkeys(thicknesses))
        variants = 0
        for value in thicknesses:
            if value == "thick" or value == "medium" or value == "thin":
                variants += 1
        if variants != 3:
            return False
        else:
            return True

    # filters down the list of IDs based on the current real feel temperature
    def requirements_by_temperature(self, feels_like):
        # creates requirements of clothing thickness depending on the temperature
        thickness = ""
        outerwear_needed = False
        bottoms_type = ""
        if feels_like <= 13:
            thickness = "thick"
            outerwear_needed = True
            bottoms_type = "long"
        elif 13 < feels_like <= 20:
            thickness = "thick"
            outerwear_needed = False
            bottoms_type = "long"
        elif 20 < feels_like <= 25:
            thickness = "medium"
            outerwear_needed = False
            bottoms_types = "short"
        else:
            thickness = "thin"
            outerwear_needed = False
            bottoms_type = "short"
        return thickness, outerwear_needed, bottoms_type

    # filtering the items down by the requirements based on temperature
    def filter_by_temperature(self, thickness, bottoms_type, tops, bottoms, onepieces, occasion_id, outerwear_needed):
        # query the database to return only the items that are of the required thickness
        tops_placeholder = ", ".join("?" * len(tops))
        onepieces_placeholder = ", ".join("?" * len(onepieces))

        tops_query = f"SELECT Item_ID FROM Clothing_Items WHERE Clothing_Thickness = ? AND Item_ID IN ({tops_placeholder})"
        self.c.execute(tops_query, (thickness, *tops))
        filtered_tops = [row[0] for row in self.c.fetchall()]

        onepieces_query = f"SELECT Item_ID FROM Clothing_Items WHERE Clothing_Thickness = ? AND Item_ID IN ({onepieces_placeholder})"
        self.c.execute(onepieces_query, (thickness, *onepieces))
        filtered_onepieces = [row[0] for row in self.c.fetchall()]

        # filtering the bottoms by the required length
        bottoms_placeholder = ", ".join("?" * len(bottoms))
        if bottoms_type == "long":
            bottom_length_placeholder = ", ".join("?" * len(self.long_bottoms))
            bottoms_query = f"""SELECT Item_ID FROM Clothing_Items WHERE Item_ID IN ({bottoms_placeholder})
                                AND Clothing_Type IN ({bottom_length_placeholder})"""
            self.c.execute(bottoms_query, (*bottoms, *self.long_bottoms))
            filtered_bottoms = [row[0] for row in self.c.fetchall()]
        else:
            bottom_length_placeholder = ", ".join("?" * len(self.short_bottoms))
            bottoms_query = f"""SELECT Item_ID FROM Clothing_Items WHERE Item_ID IN ({bottoms_placeholder})
                                AND Clothing_Type IN ({bottom_length_placeholder})"""
            self.c.execute(bottoms_query, (*bottoms, *self.short_bottoms))
            filtered_bottoms = [row[0] for row in self.c.fetchall()]

        tops_and_bottoms = [filtered_tops, filtered_bottoms]
        if filtered_onepieces:
            chosen_ids = self.determine_onepiece(filtered_onepieces, tops, occasion_id)
            if len(chosen_ids) == 0:
                return tops_and_bottoms
            else:
                return chosen_ids
        else:
            return tops_and_bottoms

    # determines if the outfit should consist of a top and bottom or a one-piece item
    def determine_onepiece(self, filtered_onepieces, tops, occasion_id):
        chosen_ids = []
        no_colour_preference = ["FM", "FE", "FP", "RE",
                                "HP"]  # the list of occasion IDs where there is no need for colour filtering
        options = ["tops", "onepiece"]
        if len(filtered_onepieces) != 0:
            base = random.choice(options)
            print(base)
            if base == "onepiece" and occasion_id in no_colour_preference:
                # check exactly what clothing type each ID is
                onepiece_type_query = "SELECT Item_ID, Clothing_Type FROM Clothing_Items WHERE Item_ID = ?"
                onepiece_types = []
                onepieces_and_ids = []
                for item in filtered_onepieces:
                    self.c.execute(onepiece_type_query, (item,))
                    response = self.c.fetchall()
                    onepiece_types.append(response[0][1])
                    onepieces_and_ids.append(response[0])
                unique_types = list(dict.fromkeys(onepiece_types))
                onepiece = random.choice(unique_types)

                # picks a top to be worn underneath if dungarees was chosen and appends IDs of both items to the list
                if onepiece == "dungarees":
                    chosen_ids.append(random.choice(tops))
                    chosen_ids.append(random.choice([pair[0] for pair in onepieces_and_ids if pair[1] == "dungarees"]))
                    return chosen_ids
                else:
                    # returns ID of the chosen one-piece item
                    chosen_ids.append(random.choice([pair[0] for pair in onepieces_and_ids if pair[1] == onepiece]))
                    return chosen_ids
            elif base == "onepiece" and occasion_id not in no_colour_preference:
                # checks if there is a one-piece item with an appropriate colour for the occasion
                check_onepiece = self.check_onepiece_colour(filtered_onepieces, occasion_id)
                if len(check_onepiece) != 0:
                    return random.choice(check_onepiece)
                else:
                    return chosen_ids
            else:
                return chosen_ids
        else:
            return chosen_ids

    # checks if there are one-piece items that are in a suitable colour for the occasion - if not tops and bottoms are chosen
    def check_onepiece_colour(self, onepieces, occasion_id):
        appropriate_ids = []
        onepiece_placeholder = ", ".join("?" * len(onepieces))
        occasion_colour = """SELECT Appropriate_Colour FROM Occasion_Colours WHERE Occasion_ID = ?"""
        item_colour = f"""SELECT Primary_Colour FROM Clothing_Items WHERE Item_ID in ({onepiece_placeholder})"""
        self.c.execute(occasion_colour, (occasion_id,))
        appropriate_colours = [row[0] for row in self.c.fetchall()]
        self.c.execute(item_colour, *onepieces)
        item_colours = [row[0] for row in self.c.fetchall()]
        for count, colour in enumerate(item_colours):
            if colour in appropriate_colours:
                appropriate_ids.append(onepieces[count])

        return appropriate_ids

    # decides if colour filtering needs to be applied, dependent on if one-pieces were chosen or not
    def call_colour_filtering(self, chosen_ids, occasion, outerwear_needed, outerwear):
        # if only one list is present, a onepiece was chosen
        if len(chosen_ids) == 1:
            chosen_ids.append("None")
            if outerwear_needed and len(outerwear) != 0:
                outerwear_id = random.choice(outerwear)
                chosen_ids.append(outerwear_id)
            else:
                chosen_ids.append("None")
            self.retrieve_selected_images(chosen_ids)
            time.sleep(2)
            self.compile_images(chosen_ids)
        elif len(chosen_ids) == 2:
            no_colour_preference = ["FM", "FE", "FP", "RE",
                                    "HP"]  # the list of occasion IDs where there is no need for colour filtering
            occasion_id = self.retrieve_occasion_id(occasion)
            if occasion_id in no_colour_preference:
                self.filter_by_colour(chosen_ids[0], chosen_ids[1], outerwear_needed, outerwear)
            else:
                ids = [chosen_ids[0], chosen_ids[1]]
                self.occasion_filter_by_colour(ids, occasion_id, outerwear_needed, outerwear)

    # filters the clothing items down by colour logic
    def filter_by_colour(self, tops, bottoms, outerwear_needed, outerwear):
        # creates placeholders for the number of items there are in each category so values can be substituted in
        colour_tops_placeholders = ", ".join("?" * len(tops))
        available_tops = ""
        available_bottoms = ""

        colours = self.get_colours()  # fetches list of all colours
        colour_match = False
        while not colour_match:
            if len(colours) == 0:
                self.create_non_colour_coordinated_outfit(tops, bottoms, outerwear, outerwear_needed)
                break
            else:
                # picks a random main colour
                main_colour = random.choice(colours)
                print(main_colour)
                colours.remove(main_colour)

                # checks if there are tops available in the main colour
                available_tops = self.fetch_colour_suitable_items(main_colour, tops)

                # selects the colours that match with the main colour
                query = "SELECT Matching_Colour FROM Colour_Combos WHERE Primary_Colour = ?"
                self.c.execute(query, (main_colour,))
                matching_colours = [row[0] for row in self.c.fetchall()]
                random.shuffle(matching_colours)

                if len(available_tops) != 0:
                    # if there are tops in the main colour, check each matching colour to see if there are bottoms in a matching colour
                    for colour in matching_colours:
                        print("Checking match colour", colour)
                        available_bottoms = self.fetch_colour_suitable_items(colour, bottoms)
                        # if there are then a colour match has been made, the image creation function is called and the program breaks out of the loop
                        if len(available_bottoms) != 0:
                            colour_match = True
                            break
                else:
                    # checks if there are bottoms available in the main colour
                    available_bottoms = self.fetch_colour_suitable_items(main_colour, bottoms)
                    if len(available_bottoms) != 0:
                        available_tops = ""
                        for colour in matching_colours:
                            print("Checking match colour", colour)
                            available_tops = self.fetch_colour_suitable_items(colour, tops)
                            if len(available_tops) != 0:
                                colour_match = True
                                break

        if colour_match:
            ids_to_be_compiled = [random.choice(available_tops), random.choice(available_bottoms)]
            if outerwear_needed and len(outerwear) != 0:
                ids_to_be_compiled.append(random.choice(outerwear))
            else:
                ids_to_be_compiled.append("None")
            self.retrieve_selected_images(ids_to_be_compiled)
            time.sleep(1)
            self.compile_images(ids_to_be_compiled)

    # fetches IDs from a passed in list that match the required colour
    def fetch_colour_suitable_items(self, colour, item_list):
        item_placeholder = ", ".join("?" * len(item_list))
        query = f"SELECT Item_ID FROM Clothing_Items WHERE Primary_Colour = ? AND Item_ID IN ({item_placeholder})"
        self.c.execute(query, (colour, *item_list))
        available_items = [row[0] for row in self.c.fetchall()]
        print(available_items)
        return available_items

    # if an occasion was selected which requires more specific colours to be worn, this function is called
    def occasion_filter_by_colour(self, clothing_ids, occasion_id, outerwear_needed, outerwear):
        top_colours = self.get_unique_colours(clothing_ids[0])
        bottom_colours = self.get_unique_colours(clothing_ids[1])
        available_tops = ""
        available_bottoms = ""

        # selects matching colour combinations where both colours are also appropriate for the occasion
        colour_combo_statement = """SELECT Primary_Colour, Matching_Colour FROM Colour_Combos
                        JOIN Occasion_Colours ON Occasion_Colours.Appropriate_Colour = Colour_Combos.Primary_Colour
                        WHERE Occasion_Colours.Occasion_ID = ?
                            AND EXISTS (
                                SELECT 1
                                FROM Occasion_Colours Occasion_Colours2
                                WHERE Occasion_Colours2.Occasion_ID = Occasion_Colours.Occasion_ID
                                AND Occasion_Colours2.Appropriate_Colour = Colour_Combos.Matching_Colour
                                );"""

        self.c.execute(colour_combo_statement, (occasion_id,))
        results = [record for record in self.c.fetchall()]
        if results:
            random.shuffle(results)
            for match in results:
                colour1 = match[0]
                colour2 = match[1]
                # checks if there are items that match the required colour combination
                if colour1 in top_colours and colour2 in bottom_colours:
                    available_tops = self.fetch_colour_suitable_items(colour1, clothing_ids[0])
                    available_bottoms = self.fetch_colour_suitable_items(colour2, clothing_ids[1])
                    break
                elif colour2 in top_colours and colour1 in bottom_colours:
                    available_tops = self.fetch_colour_suitable_items(colour2, clothing_ids[0])
                    available_bottoms = self.fetch_colour_suitable_items(colour1, clothing_ids[1])
                    break
            if len(available_tops) != 0 and len(available_bottoms) != 0:
                if outerwear_needed and len(outerwear) !=0:
                    item_ids = [random.choice(available_tops), random.choice(available_bottoms),
                                random.choice(outerwear)]
                else:
                    item_ids = [random.choice(available_tops), random.choice(available_bottoms), "None"]
                self.retrieve_selected_images(item_ids)
                time.sleep(1)
                self.compile_images(item_ids)
            else:
                self.error_not_sufficient()
        else:
            self.error_not_sufficient()

    # creates an outfit that fits occasion and temperature requirements, but not necessarily colour
    def create_non_colour_coordinated_outfit(self, tops, bottoms, outerwear, outerwear_needed):
        ids = [random.choice(tops), random.choice(bottoms)]
        if outerwear_needed and len(outerwear) != 0:
            ids.append(random.choice(outerwear))
        else:
            ids.append("None")
        self.retrieve_selected_images(ids)
        time.sleep(1)
        self.compile_images(ids)

    # fetches the list of unique colours of each of the clothing items passed in
    def get_unique_colours(self, clothing_items):
        colour_query = """SELECT Primary_Colour FROM Clothing_Items WHERE Item_ID = ?"""
        duplicate_colours = []
        for item in clothing_items:
            self.c.execute(colour_query, (item,))
            response = self.c.fetchall()
            for count in response:
                for item in count:
                    duplicate_colours.append(item)

        return list(dict.fromkeys(duplicate_colours))

    # fetches the list of all possible colours from the text file
    def get_colours(self):
        colours = []
        with open("C:/Users/jasmi/PycharmProjects/OutfitGenie/app-text-files/clothing_colours.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                colours.append(line.strip())
        colours = sorted(colours)
        return colours

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

    # returns the images of the items that were chosen to be in the outfit
    def retrieve_selected_images(self, item_ids):
        print(item_ids)
        # checks for existing images and deleting them before adding a new image
        for file in os.listdir("temp-item-images"):
            file_path = os.path.join("temp-item-images", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("deleted images in temp-item-images")
        image_query = """SELECT Clothing_Image FROM Clothing_Items WHERE Item_ID = ?"""
        # fetches each of the BLOBs for the item_IDs and saves them to a temporary folder
        for num, item in enumerate(item_ids):
            if item != "None":
                print(item)
                self.c.execute(image_query, (item,))
                response = self.c.fetchall()
                blob_img = response[0][0]
                img = Image.open(io.BytesIO(blob_img))
                img.save("C:/Users/jasmi/PycharmProjects/OutfitGenie/temp-item-images/item" + str(num) + ".png")
        print("saved new images")

    # item IDs have to be passed in the order: top, bottoms, outerwear
    def compile_images(self, item_ids):
        # checks for existing images and deleting them before adding a new image
        for file in os.listdir("temp-outfit-images"):
            file_path = os.path.join("temp-outfit-images", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("deleted images in temp-outfit-images")
        item_x_coords = [35, 35,
                         250]  # x coordinates for where the top left corner of the image will be (different for each item)
        item_y_coords = [5, 280, 40]  # the same but for the y coordinates
        num_items = len(item_ids)
        background = Image.open("app-images/White_Bg.png")  # standard white background to place the item images on
        resized_bg = background.resize((500, 650))  # resizes the background to display

        # loops through the items and places them on the white background according to the coordinates above
        for i in range(num_items):
            if item_ids[i] != "None":
                overlay_image = self.resize_image("temp-item-images/item" + str(i) + ".png")
                resized_bg.paste(overlay_image, (item_x_coords[i], item_y_coords[i]), overlay_image)
                resized_bg.save("temp-outfit-images/newoutfit.png")

        # opens the window for the user to save the generated outfit
        if self.outfit_confirmation_window is not None:
            self.outfit_confirmation_window.destroy()
            self.outfit_confirmation()
        else:
            self.outfit_confirmation()

    # resizes the image to fit the background according to its original aspect ratio
    def resize_image(self, image_path):
        overlay_image = Image.open(image_path)
        original_width = overlay_image.size[0]
        scale = (250 / float(original_width))
        height = int((float(overlay_image.size[1]) * float(scale)))
        resized_overlay = overlay_image.resize((250, height))

        return resized_overlay

    # creates a window for the user to decide if they want to keep the generated outfit or not
    def outfit_confirmation(self):
        self.outfit_confirmation_window = tk.Toplevel()
        self.outfit_confirmation_window.withdraw()
        self.outfit_confirmation_window.title("Save Outfit")
        self.outfit_confirmation_window.config(bg="#dcf5df")
        cw.centrewin(self.outfit_confirmation_window, 600, 800)

        # creating frames to contain the widgets in the window
        headingFrame = tk.Frame(self.outfit_confirmation_window, bg="#dcf5df")
        imageFrame = tk.Frame(self.outfit_confirmation_window, bg="#dcf5df")
        buttonsFrame = tk.Frame(self.outfit_confirmation_window, bg="#dcf5df")

        # creating a heading instructing the user on the purpose of the window
        headingLabel = tk.Label(headingFrame, text="Save Outfit?", font=("Montserrat ExtraBold", 20), bg="#dcf5df", fg="#969696")
        headingLabel.pack()

        # creating the image of the outfit to be displayed to the user
        temp_image = Image.open(self.newoutfit_path)
        self.generatedOutfit = ImageTk.PhotoImage(temp_image)
        imageLabel = tk.Label(imageFrame, image=self.generatedOutfit, bg="#dcf5df")
        imageLabel.pack()

        # creating the buttons so the user can decide if they want to keep the outfit
        self.deleteButtonImg = tk.PhotoImage(file="app-images/DeleteButton.png")
        deleteButton = tk.Button(buttonsFrame, background="#dcf5df", borderwidth=0, command=self.outfit_confirmation_window.withdraw)
        deleteButton.config(image=self.deleteButtonImg)

        self.confirmButtonImg = tk.PhotoImage(file="app-images/ConfirmButton.png")
        confirmButton = tk.Button(buttonsFrame, background="#dcf5df", borderwidth=0, command=self.save_outfit)
        confirmButton.config(image=self.confirmButtonImg)

        deleteButton.pack(side="left", padx=(0, 30))
        confirmButton.pack(side="right", padx=(0, 30))

        headingFrame.pack()
        imageFrame.pack()
        buttonsFrame.pack()

        self.outfit_confirmation_window.deiconify()

    # saves the outfit information to the database and displays a temporary success message
    def save_outfit(self):
        # saving to table User_Outfits
        outfit_num_object = uuid.uuid4()
        outfit_num = str(outfit_num_object)
        user_id = self.get_user_id()
        now = datetime.now()
        date_created = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.newoutfit_path, "rb") as f:
            blobData = f.read()
        insertion_query = """INSERT INTO User_Outfits (Outfit_ID, User_ID, Date_Created, Outfit_Image) VALUES (?,?,?,?)"""
        self.c.execute(insertion_query, (outfit_num, user_id, date_created, blobData))

        # saving to table Outfit_Occasions
        occasion = self.occasion.get()
        occasion_id = self.retrieve_occasion_id(occasion)
        occasion_insert = """INSERT INTO Outfit_Occasions (Outfit_ID, Occasion_ID) VALUES (?,?)"""
        self.c.execute(occasion_insert, (outfit_num, occasion_id))
        self.conn.commit()

        self.outfit_confirmation_window.destroy()
        self.successMessageFrame.place(x=0, y=770, relwidth=1)
