import sqlite3
import tkinter as tk
from tkinter import ttk
import CentreWindow as cw
import os
from datetime import datetime
import ItemViewer as itemview
from PIL import ImageTk, Image

# custom button class to allow the outfit_id to be tied to each button
class OutfitButton(tk.Button):
    def __init__(self, parent, outfit_id, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.outfit_id = outfit_id


class ViewOutfits(itemview.ViewUserItems):
    def __init__(self, parent):
        # instantiating commonly used variables
        self.parent = parent
        self.window = None
        self.style = ttk.Style()
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()
        self.user_id = self.get_user_id()

        # variable for tracking presence of attribute viewing window
        self.attribute_window = None

        # containers for the widgets on the screen
        self.headerCont = None
        self.scrollCont = None
        self.outfitCanvas = None
        self.outfitsCont = None

        # variables for holding the widgets being created
        self.backButtonImg = None
        self.backButton = None
        self.scrollbar = None
        self.emptyLabel = None

        # variables for tracking outfit button elements
        self.outfit_borders = []
        self.outfit_buttons = []
        self.outfit_images = []

        # variables for tracking the actions of a viewer window
        self.type = None
        self.outfit_id = None

        # calls the method for creating the window
        self.start()

    # creates the window and calls the method to centre it
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        cw.centrewin(self.window, 600, 800)
        self.window.title("Outfit View")
        self.window.configure(background="#f5a7a2")
        self.create_widgets()
        self.window.deiconify()

    def create_widgets(self):
        # configuring the style for frames
        self.style.configure("OutfitViewer.TFrame", background="#f5a7a2")

        # container for back button
        self.headerCont = ttk.Frame(self.window,
                                    style="OutfitViewer.TFrame",
                                    height=50)
        self.headerCont.pack(anchor="nw")

        # widgets to create back button
        self.backButtonImg = tk.PhotoImage(file="app-images/BackButton.png")
        self.backButton = tk.Button(self.headerCont,
                                    background="#f5a7a2",
                                    borderwidth=0,
                                    command=self.close_window)
        self.backButton.config(image=self.backButtonImg)
        self.backButton.pack(side="left")

        # container for scrollable section
        self.scrollCont = ttk.Frame(self.window, style="OutfitViewer.TFrame")

        # scrollable region created by a canvas
        self.outfitCanvas = tk.Canvas(self.scrollCont, background="#f5a7a2", borderwidth=0)
        self.outfitCanvas.pack(side="left", fill="both", expand=True)

        # binds the scrollbar and its movement to the canvas
        self.scrollbar = ttk.Scrollbar(self.scrollCont, orient="vertical", command=self.outfitCanvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # configures the canvas to be in line with the scrollbar when moved, and binds the canvas so whenever its dimensions change
        # i.e. the configure event occurs, the scroll region updates
        self.outfitCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.outfitCanvas.bind("<Configure>",
                               lambda e: self.outfitCanvas.configure(scrollregion=self.outfitCanvas.bbox("all")))

        # creates frame containing all the items
        self.outfitsCont = ttk.Frame(self.outfitCanvas, borderwidth=0, style="OutfitViewer.TFrame")
        self.outfitCanvas.create_window((0, 0), window=self.outfitsCont, anchor="nw")

        # label that displays if there are no images to be displayed
        self.emptyLabel = tk.Label(self.outfitsCont,
                                   background="#f5a7a2",
                                   font=("Montserrat Bold", 15),
                                   foreground="#6B6B6B",
                                   text="No outfits saved.")

        # calls the function to dynamically create the buttons and packs the container for the scrolling portion of the menu
        self.create_buttons()
        self.scrollCont.pack(fill="both", expand=True)

    # fetches images of the outfits from the database and saves them to a temporary folder
    def fetch_and_save_images(self):
        total_images = 0
        query = "SELECT Outfit_Image FROM User_Outfits WHERE User_ID = ?"
        self.c.execute(query, (self.user_id,))
        for count, record in enumerate(self.c.fetchall()):
            path = "temp-outfit-images/temp-viewing/outfit{}.png".format(count)
            with open(path, "wb") as f:
                f.write(record[0])
            total_images += 1
        print(total_images)
        return total_images

    def resize_image(self, images):
        for count in range(images):
            path = "temp-outfit-images/temp-viewing/outfit{}.png".format(count)
            tb_cropped = Image.open(path)
            newimage = tb_cropped.resize((260, 338))
            newimage.save("temp-outfit-images/temp-viewing-resized/outfit{}.png".format(count))
            os.remove("temp-outfit-images/temp-viewing/outfit{}.png".format(count))

    # fetches the IDs of the outfits and saves them to a list to be passed in during button creation to allow attributes
    # to be referenced in the future
    def fetch_outfit_ids(self):
        query = "SELECT Outfit_ID FROM User_Outfits WHERE User_ID = ?"
        self.c.execute(query, (self.user_id,))
        all_ids = [item[0] for item in self.c.fetchall()]
        return all_ids

    # dynamically creates the buttons depending on the number of outfits available
    def create_buttons(self):
        # clears the temporary directory of any images that were left over before fetching new images
        for file in os.listdir("temp-view-items"):
            file_path = os.path.join("temp-view-items", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # calls the functions for fetching the images and IDs of the outfits
        num_images = self.fetch_and_save_images()
        self.resize_image(num_images)
        outfit_ids = self.fetch_outfit_ids()

        # if there aren't any images to be shown, pack a message for the user
        if num_images == 0:
            self.emptyLabel.pack(padx=215, pady=330)

        # sets the number of buttons that can be placed on each row
        max_row = 2
        column_count = 0
        row_count = 0

        # dynamically generating buttons
        for count in range(num_images):
            path = "temp-outfit-images/temp-viewing-resized/outfit{}.png".format(count)

            # creates the elements that form a button
            temp_image = tk.PhotoImage(file=path)
            self.outfit_images.append(temp_image)
            border = tk.Frame(self.outfitsCont,
                              highlightbackground="#BDBDBD",
                              highlightthickness=3,
                              bd=0)
            button = OutfitButton(border,
                                  background="#FFFFFF",
                                  outfit_id=outfit_ids[count])
            button.bind("<Button-1>", self.view_attributes)
            button.config(image=self.outfit_images[count])

            # saving the elements to respective lists to prevent garbage collection
            self.outfit_borders.append(border)
            self.outfit_buttons.append(button)

            # adding the buttons to their container
            button.pack()
            border.grid(column=column_count, row=row_count, ipadx=10, ipady=3)
            column_count += 1
            if column_count == max_row:
                row_count += 1
                column_count = 0

    # fetches the user's ID for further database queries
    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id

    # called when the buttons displaying the outfits are pressed
    # for showing the attributes of an outfit
    def view_attributes(self, event):
        button = event.widget
        self.outfit_id = button.outfit_id
        self.type = "outfit"

        # defining the queries
        image_query = "SELECT Outfit_Image FROM User_Outfits WHERE Outfit_ID = ?"
        date_query = "SELECT Date_Created FROM User_Outfits WHERE Outfit_ID = ?"
        occasion_id_query = "SELECT Occasion_ID FROM Outfit_Occasions WHERE Outfit_ID = ?"
        occasion_id_convert_query = "SELECT Occasion_Name FROM Occasions WHERE Occasion_ID = ?"

        file_path = "temp-outfit-images/temp-viewing/temp-attribute/temp0.png"
        if os.path.isfile(file_path):
            os.remove(file_path)

        # fetching image
        self.c.execute(image_query, (self.outfit_id,))
        for row in self.c.fetchall():
            with open(file_path, "wb") as f:
                f.write(row[0])

        # fetching and formatting date
        self.c.execute(date_query, (self.outfit_id,))
        date = [item[0] for item in self.c.fetchall()]
        date_object = datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        formatted_date = date_object.strftime("%d-%m-%y")

        # fetching all occasions
        self.c.execute(occasion_id_query, (self.outfit_id,))
        occasion_ids = [item[0] for item in self.c.fetchall()]
        occasion_names = []
        for value in occasion_ids:
            self.c.execute(occasion_id_convert_query, (value,))
            for row in self.c.fetchall():
                for occasion in row:
                    occasion_names.append(occasion)

        # checking if a window displaying the attributes of a different item is already open
        # if it is, it closes it, before creating a new one
        if self.attribute_window is not None:
            self.attribute_window.destroy()
            self.create_attributes_window(formatted_date, occasion_names, file_path)
        else:
            self.create_attributes_window(formatted_date, occasion_names, file_path)

    # closes the window when the back button is pressed
    def close_window(self):
        self.window.withdraw()
