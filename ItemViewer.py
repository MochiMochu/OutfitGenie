import sqlite3
import tkinter as tk
from tkinter import ttk
import CentreWindow as cw
import os
from datetime import datetime
from PIL import Image, ImageTk


class ExpandingFilters(tk.Frame):
    def __init__(self, parent, menu_title, filters, grid_row, expanded, update_msg, update_images):
        super().__init__(parent)
        # creating variables that will be used by the class
        self.parent = parent
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()
        self.style = ttk.Style()
        self.checkbox_values = []

        # creating variables for the passed in parameters
        self.update_scrollbar = update_msg
        self.alert_update = update_images
        self.is_expanded = expanded
        self.menu_title = menu_title
        self.filters = filters

        self.style.configure("Viewer.TCheckbutton", font=("Montserrat", 8), background="#dbdbdb")
        self.widgetCont = tk.Frame(self.parent, background="#dbdbdb")
        self.checkboxCont = tk.Frame(self.widgetCont, background="#dbdbdb")

        self.menu_heading = tk.Label(self.widgetCont, text=self.menu_title, font=("Montserrat Bold", 11),
                                     background="#dbdbdb", width=15)
        self.menu_heading.bind("<Button-1>", self.toggle_menu)
        self.menu_heading.grid()

        for count, item in enumerate(self.filters):
            temp_variable = tk.IntVar(value=0)
            filter_box = ttk.Checkbutton(self.checkboxCont, text=item, command=self.alert_changes,
                                         variable=temp_variable,
                                         style="Viewer.TCheckbutton")
            self.checkbox_values.append(temp_variable)
            filter_box.grid(row=count, column=0, sticky="w")

        self.widgetCont.grid(row=grid_row, sticky="w", ipady=7)
        self.toggle_menu()

    # alerts the parent window that there were changes made to checkboxes
    def alert_changes(self):
        self.alert_update()

    # returns the values of the ticked checkboxes
    def update_images(self):
        checkbox_values = []
        checked_filters = []
        for cb in self.checkbox_values:
            checkbox_values.append(cb.get())
        for counter, value in enumerate(checkbox_values):
            if value == 1:
                checked_filters.append(self.filters[counter])
        checked_filters = [item.strip() for item in checked_filters]
        if not checked_filters:
            checked_filters.append("empty")

        return checked_filters

    def toggle_menu(self, event=None):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.checkboxCont.grid()
            self.update_scrollbar()
        else:
            self.checkboxCont.grid_remove()
            self.checkboxCont.grid_forget()
            self.update_scrollbar()
            self.parent.update_idletasks()


# slightly adapted class for buttons to allow the item_id of the item it's displaying to be stored with it
class ClothingButton(tk.Button):
    def __init__(self, parent, item_id, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.item_id = item_id


class ViewUserItems:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.style = ttk.Style()
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()
        self.temp_image = None
        self.item_images = None

        # variables for containers
        self.headerWidgets = None
        self.filterCont = None
        self.scrollCont = None
        self.leftWidgets = None
        self.itemCanvas = None
        self.itemCont = None
        self.successFrame = None

        # variables for widgets
        self.backButtonImg = None
        self.backButton = None
        self.scrollbar = None

        # integer variables to track values of the checkbox filters
        self.item_buttons = None
        self.item_borders = None
        self.all_filter_menus = None

        # tracking existence of attribute viewing window
        self.attribute_window = None

        # variable holding image for item deletion button
        self.deleteItemImg = None

        # variable tracking what kind of attribute window to show
        self.item_id = None
        self.type = None
        self.outfit_id = None

        self.start()

    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        cw.centrewin(self.window, 600, 800)
        self.window.title("Item View")
        self.window.configure(background="#f6deff")
        self.create_widgets()
        self.window.deiconify()

    # creates the widgets for the screen
    def create_widgets(self):
        # configures the styles for the ttk widgets
        self.style.configure("Viewer.TFrame", background="#dbdbdb", relief="ridge")
        self.style.configure("Cont.TFrame", background="#f6deff")

        # create container for holding all widgets that will scroll
        self.scrollCont = ttk.Frame(self.window, style="Cont.TFrame")

        # CREATING THE REGION THAT WILL HOLD THE CLOTHING ITEMS

        # scrollable region created by a canvas
        self.itemCanvas = tk.Canvas(self.scrollCont, background="#f6deff", borderwidth=0)
        self.itemCanvas.pack(side="left", fill="both", expand=True)

        # binds the scrollbar and its movement to the canvas
        self.scrollbar = ttk.Scrollbar(self.scrollCont, orient="vertical", command=self.itemCanvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # configures the canvas to be in line with the scrollbar when moved, and binds the canvas so whenever its dimensions change
        # i.e. the configure event occurs, the scroll region updates
        self.itemCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.itemCanvas.bind("<Configure>",
                             lambda e: self.itemCanvas.configure(scrollregion=self.itemCanvas.bbox("all")))

        # creates frame containing all the items
        self.itemCont = ttk.Frame(self.itemCanvas, borderwidth=0, style="Cont.TFrame")
        self.itemCanvas.create_window((0, 0), window=self.itemCont, anchor="nw")

        ids = self.fetch_all_ids()
        self.create_clothing_buttons(ids)

        # CREATES THE FILTERS FOR SORTING THE ITEMS

        # container to make the filters independent to the items
        self.leftWidgets = ttk.Frame(self.window, style="Cont.TFrame")

        # creates the frame that will contain the filters for viewing different types of items
        self.filterCont = ttk.Frame(self.leftWidgets, borderwidth=3, style="Viewer.TFrame")

        # creates the button to close the window and return to the main wardrobe menu
        self.backButtonImg = tk.PhotoImage(file="app-images/BackButton.png")
        self.backButton = tk.Button(self.leftWidgets,
                                    background="#f6deff",
                                    borderwidth=0,
                                    command=self.close_window)
        self.backButton.config(image=self.backButtonImg)

        # creates the expanding menus for the filter options
        user_id = self.get_user_id()
        all_categories = self.pad_filters()
        category_keys = list(all_categories.keys())
        self.all_filter_menus = []
        for count, key in enumerate(category_keys):
            category_filters = all_categories[key]["filters"][0]
            filter_menu = ExpandingFilters(self.filterCont, all_categories[key]["title"], category_filters, count,
                                           False, self.update_scrollbar, self.check_all_checkboxes)
            self.all_filter_menus.append(filter_menu)

        # packs all widgets into the screen
        self.backButton.grid(column=0, row=0, sticky="nw", ipady=20)
        self.filterCont.grid(column=0, row=1)
        self.leftWidgets.pack(side="left")
        self.scrollCont.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=(10, 0))

    # creates the buttons depending on the number of items
    def create_clothing_buttons(self, ids):
        # deletes any existing images from the folder
        for file in os.listdir("temp-view-items"):
            file_path = os.path.join("temp-view-items", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        num_items = self.fetch_item_images(ids)
        max_row = 2
        column_count = 0
        row_count = 0
        self.item_buttons = []
        self.item_borders = []
        self.item_images = []

        for count in range(num_items):
            path = "temp-view-items/item{}.png".format(count)
            temp_image = tk.PhotoImage(file=path)
            self.item_images.append(temp_image)
            border = tk.Frame(self.itemCont,
                              highlightbackground="#BDBDBD",
                              background="#FFFFFF",
                              highlightthickness=3,
                              bd=0)
            button = ClothingButton(border,
                                    background="#FFFFFF",
                                    borderwidth=0,
                                    item_id=ids[count])
            button.bind("<Button-1>", self.view_attributes)
            button.config(image=self.item_images[count])
            button.pack()
            border.grid(column=column_count, row=row_count, ipadx=16, ipady=3)
            self.item_buttons.append(button)
            self.item_borders.append(border)
            column_count += 1
            if column_count == max_row:
                row_count += 1
                column_count = 0

    # function called by a checkbutton that fetches the statuses of all other checkbuttons when called
    def check_all_checkboxes(self):
        new_filters = []
        for menu in self.all_filter_menus:
            new_filters.append(menu.update_images())
        self.fetch_item_ids(new_filters)

    # retrieves the item_ids of the items that fit the applied filters
    def fetch_item_ids(self, checked_filters):
        type_queried = False
        colour_queried = False
        occasion_queried = False
        type_ids = set()
        colour_ids = set()
        occasion_ids = set()
        user_id = self.get_user_id()
        if checked_filters[0][0] != "empty":
            type_filters = ", ".join("?" * len(checked_filters[0]))
            types_table_query = f"""SELECT Item_ID FROM Clothing_Items
                                                    JOIN Broader_Types ON (Broader_Types.Specific_Type = Clothing_Items.Clothing_Type
                                                    AND Broader_Types.Category in ({type_filters}))
                                                    WHERE User_ID = ?"""
            self.c.execute(types_table_query, (*checked_filters[0], user_id))
            type_ids = {item[0] for item in self.c.fetchall()}
            type_queried = True
        if checked_filters[1][0] != "empty":
            colour_filters = ", ".join("?" * len(checked_filters[1]))
            colour_table_query = f"""SELECT Item_ID FROM Clothing_Items
                                                    JOIN Broader_Colours ON (Broader_Colours.Specific_Colour = Clothing_Items.Primary_Colour
                                                    AND Broader_Colours.General_Colour in ({colour_filters}))
                                                    WHERE User_ID = ?"""
            self.c.execute(colour_table_query, (*checked_filters[1], user_id))
            colour_ids = {item[0] for item in self.c.fetchall()}
            colour_queried = True
        if checked_filters[2][0] != "empty":
            occasion_filters = ", ".join("?" * len(checked_filters[2]))
            occasion_table_query = f"""WITH all_user_items AS (
                                            SELECT Item_ID FROM Clothing_Items WHERE User_ID = ?
                                            ),
                                           occasion_suitable_items AS (
                                            SELECT Item_ID FROM Clothing_Occasions
                                            JOIN Broader_Occasions ON (Broader_Occasions.Specific_Occasion = Clothing_Occasions.Occasion_ID
                                            AND Broader_Occasions.General_Occasion in ({occasion_filters}))
                                            )
                                             SELECT all_user_items.Item_ID 
                                            FROM all_user_items
                                            JOIN occasion_suitable_items ON all_user_items.Item_ID = occasion_suitable_items.Item_ID
                                            """
            self.c.execute(occasion_table_query, (user_id, *checked_filters[2]))
            occasion_ids = {item[0] for item in self.c.fetchall()}
            occasion_queried = True

        filtered_ids = self.compare_ids(type_queried, colour_queried, occasion_queried, type_ids, colour_ids,
                                        occasion_ids)
        self.update_images(list(filtered_ids))

    # compares the IDs returned from the queries to each other and creates one list of these from which images are generated
    def compare_ids(self, type_queried, colour_queried, occasion_queried, type_ids, colour_ids, occasion_ids):
        filtered_items = set()

        if type_queried and type_ids:
            if not filtered_items:
                filtered_items = type_ids
            elif type_ids:
                filtered_items.intersection_update(type_ids)
            else:
                filtered_items = []
        if colour_queried:
            if not filtered_items:
                if type_queried:
                    filtered_items = []
                else:
                    filtered_items = colour_ids
            elif colour_ids:
                filtered_items.intersection_update(colour_ids)
            else:
                filtered_items = []
        if occasion_queried:
            if not filtered_items:
                if type_queried:
                    filtered_items = []
                else:
                    filtered_items = occasion_ids
            elif occasion_ids:
                filtered_items.intersection_update(occasion_ids)
            else:
                filtered_items = []

        return filtered_items

    # executes when the checkbutton detects changes
    def update_images(self, filtered_items):
        # removes all current buttons on the screen
        for button in self.item_buttons:
            button.grid_forget()
        for frame in self.item_borders:
            frame.grid_forget()
        # creates new buttons with the list of IDs of the filtered items.
        self.create_clothing_buttons(filtered_items)

    # fetches the images of the items based on the IDs passed in
    def fetch_item_images(self, ids):
        total_images = 0
        query = "SELECT Clothing_Image FROM Clothing_Items WHERE Item_ID = ?"
        for count, id in enumerate(ids):
            self.c.execute(query, (id,))
            response = self.c.fetchall()
            path = "temp-view-items/item{}.png".format(count)
            total_images += 1
            for row in response:
                with open(path, "wb") as f:
                    f.write(row[0])
        return total_images

    # fetches all the item IDs of the user's clothing items
    def fetch_all_ids(self):
        user_id = self.get_user_id()
        query = "SELECT Item_ID FROM Clothing_Items WHERE User_ID = ?"
        self.c.execute(query, (user_id,))
        response = self.c.fetchall()
        ids = [item[0] for item in response]
        return ids

    # fetches the ID of the current user from the text file
    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id

    # updates the viewing area of the canvas
    def update_scrollbar(self):
        self.itemCanvas.configure(scrollregion=self.itemCanvas.bbox("all"))

    # closes the window when the back button is pressed
    def close_window(self):
        self.window.withdraw()

    # triggers when the button for a clothing item is clicked, retrieving the necessary information from the database
    # and calling a method for creating a window to display this information
    def view_attributes(self, event):
        # fetching identifier for button that was clicked
        button = event.widget
        self.item_id = button.item_id
        self.type = "item"

        # defining queries to be used for looking up information to display about the item
        image_query = "SELECT Clothing_Image FROM Clothing_Items WHERE Item_ID = ?"
        date_query = "SELECT Date_Created FROM Clothing_Items WHERE Item_ID = ?"
        occasion_id_query = "SELECT Occasion_ID FROM Clothing_Occasions WHERE Item_ID = ?"
        occasion_id_convert_query = "SELECT Occasion_Name FROM Occasions WHERE Occasion_ID = ?"

        # clears any previous image that was being displayed
        file_path = "temp-view-items/temp-attribute-view/temp0.png"
        if os.path.isfile(file_path):
            os.remove(file_path)

        # fetching image
        self.c.execute(image_query, (self.item_id, ))
        for row in self.c.fetchall():
            with open(file_path, "wb") as f:
                f.write(row[0])

        # fetching and formatting date
        self.c.execute(date_query, (self.item_id, ))
        date = [item[0] for item in self.c.fetchall()]
        date_object = datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        formatted_date = date_object.strftime("%d-%m-%y")

        # fetching all occasions
        self.c.execute(occasion_id_query, (self.item_id, ))
        occasion_ids = [item[0] for item in self.c.fetchall()]
        occasion_names = []
        for value in occasion_ids:
            self.c.execute(occasion_id_convert_query, (value, ))
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

    # creates the widgets and window for viewing the attributes of the clicked item
    def create_attributes_window(self, date, occasions, file_path):
        self.attribute_window = tk.Toplevel()
        self.attribute_window.withdraw()
        cw.centrewin(self.attribute_window, 500, 400)
        self.attribute_window.lift()
        self.attribute_window.title("Attributes")
        self.attribute_window.configure(bg="#fffab8")

        # create frames for organising images
        imageFrame = tk.Frame(self.attribute_window, bg="#fffab8")
        informationFrame = tk.Frame(self.attribute_window, bg="#fffab8")
        occasionsFrame = tk.Frame(informationFrame, bg="#fffab8")

        # creates widgets displaying the information
        image_to_resize = Image.open(file_path)
        resized = image_to_resize.resize((200, 266))
        self.imageObj = ImageTk.PhotoImage(resized)
        imageLabel = tk.Label(imageFrame, image=self.imageObj, bg="#ffffff")

        # creates widgets displaying the written information
        date_text = "Date Uploaded: " + date
        dateLabel = tk.Label(informationFrame,
                             font=("Montserrat Bold", 15),
                             text=date_text,
                             bg="#fffab8")
        occasions_heading = tk.Label(informationFrame,
                                     bg="#fffab8",
                                     font=("Montserrat Bold", 15),
                                     text="Suitable Occasions:")
        for occasion in occasions:
            occasionLabel = tk.Label(occasionsFrame,
                                     font=("Montserrat", 13),
                                     text=occasion,
                                     bg="#fffab8")
            occasionLabel.pack()

        # creates a button allowing the user to delete the item
        self.deleteItemImg = tk.PhotoImage(file="app-images/DeleteItemButton.png")
        deleteButton = tk.Button(informationFrame, borderwidth=0, background="#fffab8",
                                 command=self.delete_item)
        deleteButton.configure(image=self.deleteItemImg)

        self.style.configure("Alert.TFrame", background="#9c9c9c", highlightbackground="#9c9c9c",
                             highlightcolor="#9c9c9c")
        self.successFrame = ttk.Frame(self.attribute_window, style="Alert.TFrame")

        # packs all the widgets and displays the window
        imageLabel.pack()
        imageFrame.pack(side="left", padx=6)
        dateLabel.pack(pady=5)
        occasions_heading.pack(pady=5)
        occasionsFrame.pack()
        deleteButton.pack()
        informationFrame.pack(side="right", padx=(10, 3))
        self.successFrame.place_forget()
        self.attribute_window.deiconify()

    def delete_item(self):
        self.style.configure("Alert.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        if self.type == "item":
            items_query = "DELETE FROM Clothing_Items WHERE Item_ID = ?"
            occasions_query = "DELETE FROM Clothing_Occasions WHERE Item_ID = ?"
            self.c.execute(items_query, (self.item_id, ))
            self.c.execute(occasions_query, (self.item_id, ))
            self.conn.commit()
            successMessage = ttk.Label(self.successFrame, text="Item deleted", style="Alert.TLabel")
            successMessage.pack()
            self.successFrame.place(x=0, y=370, relwidth=1)
            self.parent.after(2000, self.attribute_window.destroy)
        elif self.type == "outfit":
            items_query = "DELETE FROM User_Outfits WHERE Outfit_ID = ?"
            occasions_query = "DELETE FROM Outfit_Occasions WHERE Outfit_ID = ?"
            self.c.execute(items_query, (self.outfit_id, ))
            self.c.execute(occasions_query, (self.outfit_id, ))
            self.conn.commit()
            successMessage = ttk.Label(self.successFrame, text="Outfit deleted", style="Alert.TLabel")
            successMessage.pack()
            self.successFrame.place(x=0, y=370, relwidth=1)
            self.parent.after(2000, self.attribute_window.destroy)

    # returns the list of categories and the filters in each category from a text file
    def get_filters(self):
        all_filters = {}
        in_category = None
        with open("app-text-files/all_filters.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    in_category = None
                elif in_category is None:
                    in_category = line
                    all_filters[in_category] = {"title": in_category, "filters": []}
                else:
                    all_filters[in_category]["filters"].append(line)
        all_categories = list(all_filters.keys())
        return all_filters, all_categories

    # pads the filter options, so they are aligned to the left
    def pad_filters(self):
        # extracts the list of filters outside their categories
        sorted_filters, category_titles = self.get_filters()
        all_filters = []
        category_lengths = []
        for category in category_titles:
            filters = sorted_filters[category]["filters"]
            category_lengths.append(len(filters))  # list to keep track of how many filters each category has
            for item in filters:
                all_filters.append(item)

        # pads all the filters to be the same length as the longest item
        longest_filter = max(len(filter) for filter in all_filters)
        new_list = []
        for item in all_filters:
            pad_length = longest_filter - len(item)
            padded_item = item + (" " * pad_length) + (13 * " ")
            new_list.append(padded_item)

        # split the new list of padded items into the separate lists for each category
        index = 0
        new_split_list = []
        for length in category_lengths:
            end_list = length + index
            temp_list = new_list[index:end_list]
            new_split_list.append(temp_list)
            index = end_list

        # creates a new dictionary of dictionaries containing the new padded filters
        new_dictionary = {}
        for count, title in enumerate(category_titles):
            new_dictionary[title] = {"title": title, "filters": [new_split_list[count]]}

        return new_dictionary
