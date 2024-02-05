import tkinter as tk
from tkinter import ttk
import CentreWindow as cw
from rembg import remove
from PIL import Image, ImageChops
import tkinter.font as tkfont
import sqlite3


class Popup(tk.Frame):
    def __init__(self, parent, path, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.file_path = path
        self.output_path = "C:/Users/jasmi/PycharmProjects/OutfitGenie/temp-upload-image/item_rembg.png"
        self.menuStyle = ttk.Style()
        self.item_image = None
        self.window = None

        # variables for storing values of the dropdown boxes
        self.type_input = tk.StringVar(self.window)
        self.colour_input = tk.StringVar(self.window)
        self.fit_input = tk.StringVar(self.window)
        self.warmth_input = tk.StringVar(self.window)

        # variables for storing selected values in the occasion dropdown box
        self.occasion_variables = []
        self.friend_meetup = tk.IntVar(self.window)
        self.occasion_variables.append(self.friend_meetup)
        self.work_function = tk.IntVar(self.window)
        self.occasion_variables.append(self.work_function)
        self.job_interview = tk.IntVar(self.window)
        self.occasion_variables.append(self.job_interview)
        self.black_tie = tk.IntVar(self.window)
        self.occasion_variables.append(self.black_tie)
        self.family_event = tk.IntVar(self.window)
        self.occasion_variables.append(self.family_event)
        self.house_party = tk.IntVar(self.window)
        self.occasion_variables.append(self.house_party)
        self.festive_party = tk.IntVar(self.window)
        self.occasion_variables.append(self.festive_party)
        self.religious_event = tk.IntVar(self.window)
        self.occasion_variables.append(self.religious_event)
        self.wedding = tk.IntVar(self.window)
        self.occasion_variables.append(self.wedding)
        self.funeral = tk.IntVar(self.window)
        self.occasion_variables.append(self.funeral)

        # database connection variables
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()

        # variables containing values to fill the comboboxes
        self.all_items_types = self.get_item_types()
        self.all_colours = self.get_colours()
        self.all_fits = ["oversized", "baggy", "skinny", "fitted", "regular", "relaxed", "muscle fit"]
        self.all_occasions = self.get_occasions()
        self.all_warmth = ["thin", "medium", "thick"]

        # calls the start method to initialise all widgets
        self.start()

    # starts the window as a toplevel window, and temporarily hides it while the widgets are loaded
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        self.create_widgets()
        cw.centrewin(self.window, 500, 770)
        ddbox_font = tkfont.Font(family="Nirmala UI", size=12)
        self.option_add("*TCombobox*Listbox*Font", ddbox_font)
        self.window.title("Upload Image")
        self.window.configure(bg="#dabfde")
        self.window.deiconify()

    # function to remove the background of the image the user uploaded
    def remove_image_background(self):
        user_image = Image.open(self.file_path)
        output = remove(user_image)
        output.save(self.output_path)

    # crops the image around the objects and resizes to fit inside the buttons
    def crop_image(self, path):
        image = Image.open(path)
        bg = Image.new("RGBA", image.size, image.getpixel((0, 0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            cropped = image.crop(bbox)
            resized = cropped.resize((150, 200))
            resized.save(self.output_path)

    # gets the list of all item types from the text file
    def get_item_types(self):
        types = []
        with open("C:/Users/jasmi/PycharmProjects/OutfitGenie/app-text-files/clothing_types.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                types.append(line.strip())
        types = sorted(types)
        return types

    # gets the list of all colours from the respective text file
    def get_colours(self):
        colours = []
        with open("C:/Users/jasmi/PycharmProjects/OutfitGenie/app-text-files/clothing_colours.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                colours.append(line.strip())
        colours = sorted(colours)
        return colours

    # function to get list of occasions
    def get_occasions(self):
        self.c.execute("""SELECT Occasion_Name FROM Occasions""")
        response = self.c.fetchall()
        occasions = []
        for item in response:
            for value in item:
                occasions.append(value)
        return occasions

    # called by the clothing type dropdown box to filter down the list of types based on the user's search
    def update_type(self, event):
        value = event.widget.get()
        if value == "":
            self.clothing_type['values'] = self.all_items_types
        else:
            matches = []
            for item in self.all_items_types:
                if value.lower() in item.lower():
                    matches.append(item)
            self.clothing_type['values'] = matches

    # called by the clothing colour dropdown box to filter down the list of colours based on the user's search
    def update_colour(self, event):
        value = event.widget.get()
        if value == "":
            self.colour['values'] = self.all_colours
        else:
            matches = []
            for item in self.all_colours:
                if value.lower() in item.lower():
                    matches.append(item)
            self.colour['values'] = matches

    # called by the clothing fit dropdown box to filter down the list of types based on the user's search
    def update_fit(self, event):
        value = event.widget.get()
        if value == "":
            self.fit['values'] = self.all_fits
        else:
            matches = []
            for item in self.all_fits:
                if value.lower() in item.lower():
                    matches.append(item)
            self.fit['values'] = matches

    # converts item image into a blob to be saved to the database
    def convert_blob(self, path):
        with open (path, "rb") as f:
            blobData =f.read()
        return blobData

    # creates all the widgets in the window
    def create_widgets(self):
        self.remove_image_background()
        self.crop_image(self.output_path)

        # creates a box in the window displaying the user's uploaded image
        self.item_image = tk.PhotoImage(file=self.output_path)
        self.imageCont = ttk.Frame(self.window)
        self.uploadItemsBorder = tk.Frame(self.imageCont,
                                          highlightbackground="#BDBDBD",
                                          highlightthickness=3,
                                          bd=0)
        self.uploadedItemImg = tk.Label(self.uploadItemsBorder,
                                        image=self.item_image,
                                        width=150,
                                        height=200)
        self.uploadedItemImg.pack()
        self.uploadItemsBorder.pack()
        self.imageCont.pack()

        # creates frames to arrange the placements of dropdown boxes for the user to enter information about their item
        self.type_widgets = tk.Frame(self.window, width=450, height=100, background="#dabfde")
        self.colour_widgets = tk.Frame(self.window, width=450, height=100, background="#dabfde")
        self.fit_widgets = tk.Frame(self.window, width=450, height=100, background="#dabfde")
        self.occasion_widgets = tk.Frame(self.window, width=450, height=100, background="#dabfde")
        self.warmth_widgets = tk.Frame(self.window, width=450, height=100, background="#dabfde")

        # creates the widgets to be placed for the user to enter their item type
        self.clothing_type_title = tk.Label(self.type_widgets,
                                            text="Clothing Type:",
                                            font=("Nirmala UI Bold", 20),
                                            foreground="#5a6275",
                                            background="#dabfde")
        self.clothing_type_title.place(x=20, y=30)
        self.clothing_type = ttk.Combobox(self.type_widgets)
        self.clothing_type['values'] = self.all_items_types
        self.clothing_type.bind("<KeyRelease>", self.update_type)
        self.clothing_type.place(x=250, y=44)
        self.type_widgets.pack()

        # creates the widgets to be placed for the user to enter their item colour
        self.clothing_colour_title = tk.Label(self.colour_widgets,
                                              text="Primary Colour:",
                                              font=("Nirmala UI Bold", 20),
                                              foreground="#5a6275",
                                              background="#dabfde")
        self.clothing_colour_title.place(x=20, y=30)
        self.colour = ttk.Combobox(self.colour_widgets)
        self.colour['values'] = self.all_colours
        self.colour.bind("<KeyRelease>", self.update_colour)
        self.colour.place(x=250, y=44)
        self.colour_widgets.pack()

        # creates the widgets to be placed for the user to enter the fit of their item
        self.clothing_fit_title = tk.Label(self.fit_widgets,
                                           text="Item Fit:",
                                           font=("Nirmala UI Bold", 20),
                                           foreground="#5a6275",
                                           background="#dabfde")
        self.clothing_fit_title.place(x=20, y=30)
        self.fit = ttk.Combobox(self.fit_widgets)
        self.fit['values'] = self.all_fits
        self.fit.bind("<KeyRelease>", self.update_fit)
        self.fit.place(x=250, y=44)
        self.fit_widgets.pack()

        # creates the widgets to be placed for the user to enter the warmth of their item
        self.clothing_warmth_title = tk.Label(self.warmth_widgets,
                                              text="Item Warmth:",
                                              font=("Nirmala UI Bold", 20),
                                              foreground="#5a6275",
                                              background="#dabfde")
        self.clothing_warmth_title.place(x=20, y=30)
        self.warmth = ttk.Combobox(self.warmth_widgets)
        self.warmth['values'] = self.all_warmth
        self.warmth.place(x=250, y=44)
        self.warmth_widgets.pack()

        # creates the button to open the dropdown menu where the user can select occasions they may wear this item for
        self.menuStyle.configure("TMenubutton", width=30, font=('Nirmala UI Bold', 12), foreground="#5a6275")
        self.occasion_menu_button = ttk.Menubutton(self.occasion_widgets, text= "Select Occasions", style="TMenubutton")
        self.occasion_menu_button.pack()
        self.option_add("*Menu.activeBackground", "#D8D5DE")
        self.option_add("*Menu.activeForeground", "#5a6275")
        self.option_add("*Menu.font", ("Nirmala UI", 12))
        self.occasion_mb_menu = tk.Menu(self.occasion_menu_button, tearoff=0)
        self.occasion_menu_button["menu"] = self.occasion_mb_menu
        self.occasion_mb_menu.add_checkbutton(label="Black Tie Affair", variable=self.black_tie)
        self.occasion_mb_menu.add_checkbutton(label="Family Event", variable=self.family_event)
        self.occasion_mb_menu.add_checkbutton(label="Festive Party", variable=self.festive_party)
        self.occasion_mb_menu.add_checkbutton(label="Friend Meetup", variable=self.friend_meetup)
        self.occasion_mb_menu.add_checkbutton(label="Funeral", variable=self.funeral)
        self.occasion_mb_menu.add_checkbutton(label="House Party", variable=self.house_party)
        self.occasion_mb_menu.add_checkbutton(label="Job Interview", variable=self.job_interview)
        self.occasion_mb_menu.add_checkbutton(label="Religious Event", variable=self.religious_event)
        self.occasion_mb_menu.add_checkbutton(label="Wedding", variable=self.wedding)
        self.occasion_mb_menu.add_checkbutton(label="Work Function", variable=self.work_function)
        self.occasion_widgets.pack()

        # creates the two buttons for either saving the new item or cancelling the process
        self.save_button_image = tk.PhotoImage(file="C:/Users/jasmi/PycharmProjects/OutfitGenie/app-images/SaveButton.png")
        self.save_button = tk.Button(self.window,
                                     background="#dabfde",
                                     borderwidth=0,
                                     command=self.save_to_db)
        self.save_button.config(image=self.save_button_image)
        self.save_button.pack(pady=(10, 0))
        self.cancel_button_image = tk.PhotoImage(file="C:/Users/jasmi/PycharmProjects/OutfitGenie/app-images/CancelButton.png")
        self.cancel_button = tk.Button(self.window,
                                       background="#dabfde",
                                       borderwidth=0,
                                       command=self.window.withdraw)
        self.cancel_button.config(image=self.cancel_button_image)
        self.cancel_button.pack()


    def save_to_db(self):
        type = self.type_input.get()
        colour = self.colour_input.get()
        fit = self.fit_input.get()
        warmth = self.warmth_input.get()
        occasions_check = False
        for variable in self.occasion_variables:
            value = variable.get()
            if value == 1:
                occasions_check = True
        if type == "":
            print("Please enter a type")
        elif colour == "":
            print("Please enter a colour")
        elif fit == "":
            print("Please enter a fit")
        elif warmth == "":
            print("Please enter the thickness of the item")
        elif not occasions_check:
            print("Please enter at least one occasion")
        else:
            image_to_upload = self.convert_blob(self.output_path)















