import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from opencage.geocoder import OpenCageGeocode  # imports the module for the weather API
import bcrypt
import CentreWindow as cw
import uuid


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class SignUpEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


class SignUpScreen(tk.Frame):
    def __init__(self, parent, user_logged_in, open_home, close_app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.geo_api = "57685bde1a7349b78f9c15209ac92d32"  # api key for geosearching
        self.window = None
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()

        # initiating variables to be used
        self.open_homescreen = open_home
        self.close_app = close_app
        self.SU_style = ttk.Style()  # for styling the ttk widgets
        self.frame_style = ttk.Style()
        self.alert_login = user_logged_in

        # initiating instance variables to be modified later
        self.SU_username = None
        self.password = None
        self.confirmed_password = None
        self.email = None
        self.location = None
        self.country = None
        self.lat = 0  # longitude to check if the location exists
        self.long = 0  # latitude " "
        self.show_password = None
        self.headerCont = None
        self.entryCont = None
        self.signUpCont = None
        self.heading = None
        self.subheading = None
        self.usernameEntry = None
        self.passwordEntry = None
        self.confirmPasswordEntry = None
        self.emailEntry = None
        self.locationEntry = None
        self.countryEntry = None
        self.SUshowPass = None
        self.SUsignUpButton = None

        # initiating the labels for error messages
        self.SUusernameTaken = None
        self.passwordNoMatch = None
        self.passwordLonger = None
        self.passwordLower = None
        self.passwordUpper = None
        self.passwordNum = None
        self.passwordSymbol = None
        self.passwordSpace = None
        self.passwordNoConfirm = None
        self.invalidEmail = None
        self.unknownLocation = None
        self.api_fail = None

        self.successCreate = None
        self.successMessage = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 850)
        self.window.title("OutfitGenie")
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.configure(bg="#ddedea")
        self.create_widgets()

    def create_widgets(self):
        self.SU_style.configure("TFrame", background="#ddedea")  # configure the frame background
        self.SU_username = tk.StringVar(self.window)
        self.password = tk.StringVar(self.window)
        self.confirmed_password = tk.StringVar(self.window)
        self.email = tk.StringVar(self.window)
        self.location = tk.StringVar(self.window)  # tk variables for storing location for weather in the user's area
        self.country = tk.StringVar(self.window)

        self.show_password = tk.BooleanVar(self.window, True)

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
        self.usernameEntry = SignUpEntry(self.entryCont, "Username", self.temp_username,
                                       font=("Nirmala UI", 12),
                                       background="#abd3cb",
                                       foreground="#9c9c9c",
                                       textvariable=self.SU_username,
                                       width=45)
        self.passwordEntry = SignUpEntry(self.entryCont, "Password", self.temp_password,
                                           font=("Nirmala UI", 12),
                                           background="#abd3cb",
                                           foreground="#9c9c9c",
                                           show="",
                                           textvariable=self.password,
                                           width=45)
        self.emailEntry = SignUpEntry(self.entryCont, "Email", self.temp_email,
                                      font=("Nirmala UI", 12),
                                      background="#abd3cb",
                                      foreground="#9c9c9c",
                                      show="",
                                      textvariable=self.email,
                                      width=45)
        self.confirmPasswordEntry = SignUpEntry(self.entryCont, "Confirm password", self.temp_confirm_password,
                                                font=("Nirmala UI", 12),
                                                background="#abd3cb",
                                                foreground="#9c9c9c",
                                                show="",
                                                textvariable=self.confirmed_password,
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
        self.SU_style.configure("TCheckbutton", background="#ddedea", font=("Montserrat", 10))
        self.SU_style.configure("TLabel", font=("Montserrat", 10), background="#ddedea")
        self.SU_style.configure("TButton", font=("Montserrat", 10))

        # widgets for the checkbox to show the password and button for submitting the user's details
        self.SUshowPass = ttk.Checkbutton(self.signUpCont,
                                          text="Show password",
                                          command=self.toggle_password,
                                          variable=self.show_password)
        self.SUsignUpButton = ttk.Button(self.signUpCont, text="Sign Up", command=self.check_inputs, width=25)

        # initiating the labels for error messages
        self.SUusernameTaken = ttk.Label(self.signUpCont, text="Error, this username has already been taken.",
                                         foreground="red")
        self.passwordNoMatch = ttk.Label(self.signUpCont, text="Error, password does not match username.",
                                           foreground="red")
        self.passwordLonger = ttk.Label(self.signUpCont, text="✖ Password must be longer than 8 letters")
        self.passwordLower = ttk.Label(self.signUpCont, text="✖ Password must contain lower case letters")
        self.passwordUpper = ttk.Label(self.signUpCont, text="✖ Password must contain upper case letters")
        self.passwordNum = ttk.Label(self.signUpCont, text="✖ Password must contain one or more numbers")
        self.passwordSymbol = ttk.Label(self.signUpCont,
                                          text="✖ Password must contain one or more special symbols (_@$#?£!;/%^&*()+=~<>.,-)")
        self.passwordSpace = ttk.Label(self.signUpCont, text="✖ Password must contain no whitespace characters")
        self.passwordNoConfirm = ttk.Label(self.signUpCont, text="Error, password entries do not match.")
        self.invalidEmail = ttk.Label(self.signUpCont, text="Error, email is used or invalid.")
        self.unknownLocation = ttk.Label(self.signUpCont, text="Error, location not found.")
        self.api_fail = ttk.Label(self.signUpCont, text="Error, unable to validate location at this time.")

        # account successful creation message widget
        self.frame_style.configure("Success.TFrame",
                                   background="#9c9c9c",
                                   highlightbackground="#9c9c9c",
                                   hightlightcolor="#9c9c9c")  # configure frame bg for success message
        self.successCreate = ttk.Frame(self.window, style="Success.TFrame")
        self.frame_style.configure("Success.TLabel", font=("Montserrat", 15), foreground="#FFFFFF",
                                   background="#9c9c9c")
        self.successMessage = ttk.Label(self.successCreate, text="Account created successfully", style="Success.TLabel")

        # packing all the widgets into their respective framesM
        self.heading.pack()
        self.subheading.pack(pady=(30, 0))
        self.headerCont.pack(pady=(150, 20))  # pack the frame containing the headers

        self.usernameEntry.pack(pady=10)
        self.passwordEntry.pack(pady=10)
        self.confirmPasswordEntry.pack(pady=10)
        self.emailEntry.pack(pady=10)
        self.locationEntry.pack(pady=10)
        self.countryEntry.pack(pady=10)
        self.entryCont.pack(pady=20)  # pack the frame containing the user entry boxes

        self.SUshowPass.pack()
        self.SUsignUpButton.pack(pady=10)
        self.signUpCont.pack(pady=(10, 0))  # pack the frame containing the bottom half of the widgets

        self.successMessage.pack()  # pack success message into frame

    # deletes the temporary text in username box
    def temp_username(self, event):
        self.usernameEntry.delete(0, "end")

    # deletes the temporary text in password box
    def temp_password(self, event):
        self.passwordEntry.delete(0, "end")
        self.show_password.set(False)
        self.passwordEntry.config(show="•")

    # deletes the temporary text in confirm password box
    def temp_confirm_password(self, event):
        self.confirmPasswordEntry.delete(0, "end")
        self.show_password.set(False)
        self.confirmPasswordEntry.config(show="•")

    # deletes the temporary text in location box
    def temp_email(self, event):
        self.emailEntry.delete(0, "end")

    # deletes the temporary text in location box
    def temp_location(self, event):
        self.locationEntry.delete(0, "end")

    # deletes the temporary text in country box
    def temp_country(self, event):
        self.countryEntry.delete(0, "end")

    # clears all errors before validating input again
    def clear_errors(self):
        self.passwordLonger.pack_forget()
        self.passwordLower.pack_forget()
        self.passwordUpper.pack_forget()
        self.passwordNum.pack_forget()
        self.passwordSymbol.pack_forget()
        self.passwordSpace.pack_forget()
        self.SUusernameTaken.pack_forget()
        self.passwordNoConfirm.pack_forget()
        self.invalidEmail.pack_forget()
        self.unknownLocation.pack_forget()
        self.api_fail.pack_forget()

    # warns the user if the username has already been taken, clears any password errors too
    def username_error(self):
        self.passwordLonger.pack_forget()
        self.passwordLower.pack_forget()
        self.passwordUpper.pack_forget()
        self.passwordNum.pack_forget()
        self.passwordSymbol.pack_forget()
        self.passwordSpace.pack_forget()
        self.SUusernameTaken.pack(pady=(5, 0))

    # function for the checkbox toggling whether the password can be seen
    def toggle_password(self):
        if self.show_password.get():  # If show is checked, reveal the password
            self.passwordEntry.config(show="")
            self.confirmPasswordEntry.config(show="")
        else:
            self.passwordEntry.config(show="•")
            self.confirmPasswordEntry.config(show="•")

    # checking user inputs by calling different functions and packing error messages if they return False
    def check_inputs(self):
        self.clear_errors()
        # checks if username already exists first
        existing_usernames = self.username_taken()
        if existing_usernames:
            # checks if password meets requirements
            flags = self.password_validity(self.password.get())
            if self.password_errors(flags):
                # checks if both entered passwords match
                password_match = self.confirm_password()
                if password_match:
                    # checks if the email is valid
                    email_valid = self.check_email()
                    if email_valid:
                        # checks if the location entered is valid
                        location_valid = self.validate_location()
                        if location_valid:
                            self.send_pass()  # saves details to database
                            self.account_success()  # shows success message
                            self.alert_login()
                            self.parent.after(1500,
                                              self.open_homescreen)  # calls function to close current window and open the home screen
                        else:
                            self.unknownLocation.pack()
                    else:
                        self.invalidEmail.pack()
                else:
                    self.passwordNoConfirm.pack()
        else:
            self.username_error()

    # regex checker to check if entered email meets basic email requirements (an @ and . to precede domain)
    def check_email(self):
        entered_email = self.email.get()
        # checks if the email is already in use
        query = "SELECT User_ID FROM Users WHERE Email = ?"
        self.c.execute(query, (entered_email, ))
        if self.c.fetchall():
            return False
        else:
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", entered_email):
                return False
            else:
                self.invalidEmail.pack_forget()
                return True

    # check if username has been taken - returns True if there are no other usernames
    def username_taken(self):
        self.SUusernameTaken.pack_forget()
        u = self.SU_username.get()
        u = u.lower()
        p = self.password.get()
        select_query = "SELECT * FROM Users where Username = ?"
        self.c.execute(select_query, (u,))
        answer = self.c.fetchall()
        items = len(answer)
        if items == 0:
            return True
        else:
            return False

    @staticmethod
    # checks whether the password meets the requirements for a secure password and passes any flags to password_errors
    def password_validity(password):
        # unpacking any previous password errors
        p = password
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
        return flags

    # checks if the user's entered location is a valid place in the world
    def validate_location(self):
        self.api_fail.pack_forget()
        self.unknownLocation.pack_forget()
        query = self.location.get() + ", " + self.country.get()
        api_success = False
        try:
            geocoder = OpenCageGeocode(self.geo_api)
            results = geocoder.geocode(query)
            api_success = True
        except:
            self.api_fail.pack()

        if api_success:
            if results and len(results):
                valid_types = ["village", "hamlet", "neighbourhood", "city", "town", "county", "region",
                               "country"]  # valid types of location
                if 'components' in results[0] and '_type' in results[0]['components'] and \
                        any(t in results[0]['components']['_type'] for t in
                            valid_types):  # checks if the location is part of the accepted types
                    self.lat = results[0]["geometry"]["lat"]  # saves the latitude
                    self.long = results[0]["geometry"]["lng"]  # saved the longitude
                    return True
                else:
                    return False
            else:
                return False

    # packs the required error labels for any password criteria that aren't met
    def password_errors(self, flags):
        self.passwordLonger.pack_forget()
        self.passwordLower.pack_forget()
        self.passwordUpper.pack_forget()
        self.passwordNum.pack_forget()
        self.passwordSymbol.pack_forget()
        self.passwordSpace.pack_forget()
        self.SUusernameTaken.pack_forget()
        for num in flags:
            if num == "0":
                return True
            else:
                if num == "1":
                    self.passwordLonger.pack()
                elif num == "2":
                    self.passwordLower.pack()
                elif num == "3":
                    self.passwordUpper.pack()
                elif num == "4":
                    self.passwordNum.pack()
                elif num == "5":
                    self.passwordSymbol.pack()
                elif num == "6":
                    self.passwordSpace.pack()

    # check if the password to be confirmed matches the one originally entered
    def confirm_password(self):
        self.passwordNoConfirm.pack_forget()
        p1 = self.password.get()  # retrieves the first password entered
        p2 = self.confirmed_password.get()  # retrieves the second password entered
        if p1 != p2:
            return False
        else:
            return True

    # retrieves the number of users already signed up in order to create the next user's ID
    def get_user_num(self):
        user_object = uuid.uuid4()
        user_number = str(user_object)
        return user_number

    # submits user details to the database
    def send_pass(self):
        u = self.SU_username.get()
        p = self.password.get()
        h_password, salt = self.hash_password_for_storage(p)
        num = self.get_user_num()
        u = u.lower()
        email = self.email.get()
        latitude = self.lat
        longitude = self.long
        conn = sqlite3.connect("OutfitGenieInfo.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Users VALUES (:id, :users, :passes, :latitude, :longitude, :salt, :email)",
                      {"id": num,
                       "users": u,
                       "passes": h_password,
                       "latitude": latitude,
                       "longitude": longitude,
                       "salt": salt,
                       "email": email}
                      )
        except sqlite3.IntegrityError as err:  # checks again if the username already exists
            if err.args != "UNIQUE constraint failed: Users.username":
                self.username_error()
        conn.commit()
        conn.close()
        self.save_username(num)  # saves the username to the current user file for later record retrieval

    @staticmethod
    def hash_password_for_storage(password):
        password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed, salt

    # saves the current user's user_id to the text file to be able to access their information later
    def save_username(self, num):
        with open("app-text-files/current_user.txt", "w") as f:
            f.write(str(num))

    # displays success of account creation
    def account_success(self):
        self.successCreate.place(x=0, y=0, relwidth=1)
