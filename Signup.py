import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from opencage.geocoder import OpenCageGeocode  # imports the module for the weather API
import bcrypt


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class SignUpEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


class SignUpScreen(tk.Frame):
    def __init__(self, parent, user_logged_in, open_home, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.geo_api = "57685bde1a7349b78f9c15209ac92d32" # api key for geosearching
        self.window = None

        # initiating variables to be used
        self.open_homescreen = open_home
        self.close_app = close_app
        self.SUstyle = ttk.Style()  # for styling the ttk widgets
        self.FrameStyle = ttk.Style()
        self.alert_login = user_logged_in

        # initiating instance variables to be modified later
        self.SUusername = None
        self.SUpassword = None
        self.confirmedPassword = None
        self.location = None
        self.country = None
        self.lat = 0  # longitude to check if the location exists
        self.long = 0  # latitude " "
        self.SUshow = None
        self.headerCont = None
        self.entryCont = None
        self.signUpCont = None
        self.heading = None
        self.subheading = None
        self.SUuserEntry = None
        self.SUpasswordEntry = None
        self.confirmPasswordEntry = None
        self.locationEntry = None
        self.countryEntry = None
        self.SUshowPass = None
        self.SUsignUpButton = None

        # initiating the labels for error messages
        self.SUusernameTaken = None
        self.SUpasswordNoMatch = None
        self.SUpasswordLonger = None
        self.SUpasswordLower = None
        self.SUpasswordUpper = None
        self.SUpasswordNum = None
        self.SUpasswordSymbol = None
        self.SUpasswordSpace = None
        self.SUpasswordNoConfirm = None
        self.unknownLocation = None

        self.successCreate = None
        self.successMessage = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("OutfitGenie")
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.configure(bg="#ddedea")
        self.window.geometry("600x800+1000+300")
        self.create_widgets()

    def create_widgets(self):
        self.SUstyle.configure("TFrame", background="#ddedea")  # configure the frame background
        self.SUusername = tk.StringVar(self.window)
        self.SUpassword = tk.StringVar(self.window)
        self.confirmedPassword = tk.StringVar(self.window)
        self.location = tk.StringVar(self.window)   # tk variables for storing location for weather in the user's area
        self.country = tk.StringVar(self.window)

        self.SUshow = tk.BooleanVar(self.window, True)

        # initiating the frames containing the widgets
        self.headerCont = ttk.Frame(self.window, height=150, width=600, style="TFrame")
        self.entryCont = ttk.Frame(self.window, height=150, width=600, style="TFrame")
        self.signUpCont = ttk.Frame(self.window, height=150, width=400, style="TFrame")

        # initiating the headings for the screen
        self.heading = ttk.Label(self.headerCont,
                                 text="Welcome to OutfitGenie.",
                                 background="#ddedea",
                                 foreground="#7E7E7E",
                                 font=("Montserrat ExtraBold", 28))
        self.subheading = ttk.Label(self.headerCont,
                                    text="Let's get you set up.",
                                    foreground="#7E7E7E",
                                    background="#ddedea",
                                    font=("Montserrat Bold", 20))

        # initiating the entry box widgets to be added to the interface
        self.SUuserEntry = SignUpEntry(self.entryCont, "Username", self.temp_username,
                                       font=("Nirmala UI", 12),
                                       background="#abd3cb",
                                       foreground="#9c9c9c",
                                       textvariable=self.SUusername,
                                       width=45)
        self.SUpasswordEntry = SignUpEntry(self.entryCont, "Password", self.temp_password,
                                           font=("Nirmala UI", 12),
                                           background="#abd3cb",
                                           foreground="#9c9c9c",
                                           show="",
                                           textvariable=self.SUpassword,
                                           width=45)
        self.confirmPasswordEntry = SignUpEntry(self.entryCont, "Confirm password", self.temp_confirm_password,
                                                font=("Nirmala UI", 12),
                                                background="#abd3cb",
                                                foreground="#9c9c9c",
                                                show="",
                                                textvariable=self.confirmedPassword,
                                                width=45)

        self.locationEntry = SignUpEntry(self.entryCont, "Town/City (for weather recommendations)", self.temp_location,
                                                font=("Nirmala UI", 12),
                                                background="#abd3cb",
                                                foreground="#9c9c9c",
                                                textvariable=self.location,
                                                width=45)

        self.countryEntry = SignUpEntry(self.entryCont, "Country", self.temp_country,
                                                font=("Nirmala UI", 12),
                                                background="#abd3cb",
                                                foreground="#9c9c9c",
                                                textvariable=self.country,
                                                width=45)
        # configuring ttk widget styles
        self.SUstyle.configure("TCheckbutton", background="#ddedea", font=("Montserrat", 10))
        self.SUstyle.configure("TLabel", font=("Montserrat", 10), background="#ddedea")
        self.SUstyle.configure("TButton", font=("Montserrat", 10))

        # widgets for the checkbox to show the password and button for submitting the user's details
        self.SUshowPass = ttk.Checkbutton(self.signUpCont,
                                          text="Show password",
                                          command=self.toggle_password,
                                          variable=self.SUshow)
        self.SUsignUpButton = ttk.Button(self.signUpCont, text="Sign Up", command=self.username_taken, width=25)

        # initiating the labels for error messages
        self.SUusernameTaken = ttk.Label(self.signUpCont, text="Error, this username has already been taken.",
                                         foreground="red")
        self.SUpasswordNoMatch = ttk.Label(self.signUpCont, text="Error, password does not match username.",
                                           foreground="red")
        self.SUpasswordLonger = ttk.Label(self.signUpCont, text="✖ Password must be longer than 8 letters")
        self.SUpasswordLower = ttk.Label(self.signUpCont, text="✖ Password must contain lower case letters")
        self.SUpasswordUpper = ttk.Label(self.signUpCont, text="✖ Password must contain upper case letters")
        self.SUpasswordNum = ttk.Label(self.signUpCont, text="✖ Password must contain one or more numbers")
        self.SUpasswordSymbol = ttk.Label(self.signUpCont,
                                          text="✖ Password must contain one or more special symbols (_@$#?£!;/%^&*()+=~<>.,-)")
        self.SUpasswordSpace = ttk.Label(self.signUpCont, text="✖ Password must contain no whitespace characters")
        self.SUpasswordNoConfirm = ttk.Label(self.signUpCont, text="Error, password entries do not match.")
        self.unknownLocation = ttk.Label(self.signUpCont, text="Error, location not found.")

        # account successful creation message widget
        self.FrameStyle.configure("Success.TFrame",
                                  background="#9c9c9c",
                                  highlightbackground="#9c9c9c",
                                  hightlightcolor="#9c9c9c") # configure frame bg for success message
        self.successCreate = ttk.Frame(self.window, style="Success.TFrame")
        self.FrameStyle.configure("Success.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.successMessage = ttk.Label(self.successCreate, text="Account created successfully", style="Success.TLabel")

        # packing all the widgets into their respective framesM
        self.heading.pack()
        self.subheading.pack(pady=(30, 0))
        self.headerCont.pack(pady=(150, 20))  # pack the frame containing the headers

        self.SUuserEntry.pack(pady=10)
        self.SUpasswordEntry.pack(pady=10)
        self.confirmPasswordEntry.pack(pady=10)
        self.locationEntry.pack(pady=10)
        self.countryEntry.pack(pady=10)
        self.entryCont.pack(pady=20)  # pack the frame containing the user entry boxes

        self.SUshowPass.pack()
        self.SUsignUpButton.pack(pady=10)
        self.signUpCont.pack(pady=(10, 0))  # pack the frame containing the bottom half of the widgets

        self.successMessage.pack()  # pack success message into frame

    # deletes the temporary text in username box
    def temp_username(self, event):
        self.SUuserEntry.delete(0, "end")

    # deletes the temporary text in password box
    def temp_password(self, event):
        self.SUpasswordEntry.delete(0, "end")
        self.SUshow.set(False)
        self.SUpasswordEntry.config(show="•")

    # deletes the temporary text in confirm password box
    def temp_confirm_password(self, event):
        self.confirmPasswordEntry.delete(0, "end")
        self.SUshow.set(False)
        self.confirmPasswordEntry.config(show="•")

    # deletes the temporary text in location box
    def temp_location(self, event):
        self.locationEntry.delete(0, "end")

    # deletes the temporary text in country box
    def temp_country(self, event):
        self.countryEntry.delete(0, "end")

    # warns the user if the username has already been taken, clears any password errors too
    def username_error(self):
        self.SUpasswordLonger.pack_forget()
        self.SUpasswordLower.pack_forget()
        self.SUpasswordUpper.pack_forget()
        self.SUpasswordNum.pack_forget()
        self.SUpasswordSymbol.pack_forget()
        self.SUpasswordSpace.pack_forget()
        self.SUusernameTaken.pack(pady=(5, 0))

    # function for the checkbox toggling whether the password can be seen
    def toggle_password(self):
        if self.SUshow.get():  # If show is checked, reveal the password
            self.SUpasswordEntry.config(show="")
            self.confirmPasswordEntry.config(show="")
        else:
            self.SUpasswordEntry.config(show="•")
            self.confirmPasswordEntry.config(show="•")

    # check if username has been taken
    def username_taken(self):
        self.unknownLocation.pack_forget() # unpacks any errors from if the location wasn't valid
        u = self.SUusername.get()
        u = u.lower()
        p = self.SUpassword.get()
        conn = sqlite3.connect("OutfitGenieInfo.db")
        c = conn.cursor()
        select_query = "SELECT * FROM Users where Username = ?"
        c.execute(select_query, (u,))
        answer = c.fetchall()
        conn.close()
        items = len(answer)
        login_details = []
        for item in answer:
            for value in item:
                login_details.append(value)
        if items == 0:
            self.password_validity()
        else:
            self.username_error()

    # checks whether the password meets the requirements for a secure password and passes any flags to password_errors
    def password_validity(self):
        # unpacking any previous password errors
        self.SUpasswordLonger.pack_forget()
        self.SUpasswordLower.pack_forget()
        self.SUpasswordUpper.pack_forget()
        self.SUpasswordNum.pack_forget()
        self.SUpasswordSymbol.pack_forget()
        self.SUpasswordSpace.pack_forget()
        self.SUusernameTaken.pack_forget()
        p = self.SUpassword.get()
        flags = []
        if len(p) <= 8:
            flags.append("1")
        if not re.search('[a-z]', p):
            flags.append("2")
        if not re.search('[A-Z]', p):
            flags.append("3")
        if not re.search('[0-9]', p):
            flags.append("4")
        if not re.search("[_@$#?£!;/%^&*()+=~<>.,{}':-]", p):
            flags.append("5")
        if re.search("\s", p):
            flags.append("6")
        if len(flags) == 0:
            flags.append("0")
        self.password_errors(flags)

    # checks if the user's entered location is a valid place in the world
    def validate_location(self):
        self.unknownLocation.pack_forget()
        geocoder = OpenCageGeocode(self.geo_api)
        query = self.location.get() + ", "+self.country.get()
        results = geocoder.geocode(query)
        if results and len(results):
            valid_types = ["village", "hamlet", "neighbourhood", "city", "town", "county", "region", "country"]  # valid types of location
            if 'components' in results[0] and '_type' in results[0]['components'] and \
                    any(t in results[0]['components']['_type'] for t in valid_types):  # checks if the location is part of the accepted types 
                self.lat = results[0]["geometry"]["lat"]  # saves the latitude
                self.long = results[0]["geometry"]["lng"]  # saved the longitude
                self.confirm_password()
            else:
                self.unknownLocation.pack()
        else:
            self.unknownLocation.pack()

    # packs the required error labels for any password criteria that aren't met
    def password_errors(self, flags):
        for num in flags:
            if num == "0":
                self.validate_location()
                break
            else:
                if num == "1":
                    self.SUpasswordLonger.pack()
                elif num == "2":
                    self.SUpasswordLower.pack()
                elif num == "3":
                    self.SUpasswordUpper.pack()
                elif num == "4":
                    self.SUpasswordNum.pack()
                elif num == "5":
                    self.SUpasswordSymbol.pack()
                elif num == "6":
                    self.SUpasswordSpace.pack()

    # check if the password to be confirmed matches the one originally entered
    def confirm_password(self):
        self.unknownLocation.pack_forget()
        p1 = self.SUpassword.get()  # retrieves the first password entered
        p2 = self.confirmedPassword.get()  # retrieves the second password entered
        if p1 != p2:
            self.SUpasswordNoConfirm.pack()  # packs the error message that the passwords don't match
        else:
            self.SUpasswordNoConfirm.pack_forget()  # removes any previously existing error messages
            self.send_pass()  # saves details to database
            self.account_success()  # shows success message
            self.alert_login()
            self.parent.after(1500, self.open_homescreen)  # calls function to close current window and open the home screen 
 
    # retrieves the number of users already signed up in order to create the next user's ID
    def get_user_num(self):
        conn = sqlite3.connect("OutfitGenieInfo.db")
        c = conn.cursor()
        c.execute("""SELECT User_ID FROM Users WHERE User_ID=(SELECT max(user_id) FROM Users)""")
        record = c.fetchall()
        conn.close()
        if record:
            user_number = record[0]
            user_number += 1
            print(user_number)
        else:
            user_number = 1
        return user_number

    # submits user details to the database
    def send_pass(self):
        u = self.SUusername.get()
        p = self.SUpassword.get()
        h_password, salt = self.hash_password_for_storage(p)
        num = self.get_user_num()
        u = u.lower()
        latitude = self.lat
        longitude = self.long
        conn = sqlite3.connect("OutfitGenieInfo.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Users VALUES (:id, :users, :passes, :latitude, :longitude, :salt)",
                      {"id": num,
                       "users": u,
                       "passes": h_password,
                       "latitude": latitude,
                       "longitude": longitude,
                       "salt": salt}
                      )
            self.SUusernameTaken.pack_forget()
        except sqlite3.IntegrityError as err:  # checks again if the username already exists
            if err.args != "UNIQUE constraint failed: Users.username":
                self.username_error()
        conn.commit()
        conn.close()
        self.save_username(u)  # saves the username to the current user file for later record retrieval

    def hash_password_for_storage(self, password):
        password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed, salt

    # saves the current user's username to the text file to be able to access their information later
    def save_username(self, u):
        with open("current_user.txt", "w") as f:
            f.write(u)

    # displays success of account creation
    def account_success(self):
        self.successCreate.place(x=0, y=0, relwidth=1)




