# import required modules and libraries
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import time
import bcrypt
import CentreWindow as cw


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class CustomEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


# initiating the main window of the application
class LoginScreen(tk.Frame):
    def __init__(self, parent, user_logged_in, open_signup, open_home, close_app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        self.window = None

        # necessary variables that aren't widgets
        self.style = ttk.Style()  # creates instance of Style class to enable ttk widget editing later
        self.frame_style = ttk.Style()  # creates a separate instance for the account success message
        self.close_and_open_home = open_home
        self.close_and_open_signup = open_signup
        self.close_app = close_app
        self.alert_login = user_logged_in

        # initiating an instance variable for every widget
        self.username = None
        self.password = None
        self.show = None
        self.userEntry = None
        self.passwordEntry = None
        self.logo = None
        self.logoImage = None
        self.btnCont = None
        self.showPass = None
        self.loginButton = None
        self.usernameNotFound = None
        self.usernameTaken = None
        self.passwordNoMatch = None
        self.successLogin = None
        self.successMessage = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        cw.centrewin(self.window, 600, 800)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#cdf3ff")
        self.window.deiconify()
        self.create_widgets()

    def create_widgets(self):
        # initiating variables to be used
        self.username = tk.StringVar(self.window)
        self.password = tk.StringVar(self.window)
        self.show = tk.BooleanVar(self.window, True)  # Boolean variable to track if "show password" is checked

        # initiating the widgets to be added to the interface
        self.userEntry = CustomEntry(self.window, "Username", self.temp_username,
                                     font=("Nirmala UI", 12),
                                     foreground="#989898",
                                     textvariable=self.username,
                                     width=45)
        self.passwordEntry = CustomEntry(self.window, "Password", self.temp_password,
                                         font=("Nirmala UI", 12),
                                         foreground="#989898",
                                         show="",
                                         textvariable=self.password,
                                         width=45)
        # creating a canvas widget in which the logo image can be created
        self.logo = tk.Canvas(self.window, width=300, height=160, background='#cdf3ff', highlightbackground="#cdf3ff")
        self.logoImage = self.get_logo()
        self.logo.create_image(152, 80, image=self.logoImage)

        # configuring ttk widgets before initiating them
        self.style.configure("TFrame", background="#cdf3ff")
        self.style.configure("TCheckbutton", background="#cdf3ff", font = ("Montserrat", 10))
        self.style.configure("TLabel", font= ("Nirmala UI", 10), background="#cdf3ff")
        self.style.configure("TButton", font= ("Montserrat", 10))
        self.btnCont = ttk.Frame(self.window, height=80, width=200)
        self.showPass = ttk.Checkbutton(self.btnCont,
                                        text="Show password",
                                        command=self.toggle_password,
                                        variable=self.show)
        self.loginButton = ttk.Button(self.btnCont, text="Login/Sign Up", command=self.sign_in, width=15)

        # labels for error messages
        self.usernameNotFound = ttk.Label(self.btnCont, text="Username not found, sign up process starting...", foreground="red")
        self.passwordNoMatch = ttk.Label(self.btnCont, text="Error, password does not match username.", foreground="red")
        # labels for error messages

        # account successful login message widget
        self.frame_style.configure("Success.TFrame", background="#9c9c9c", highlightbackground="#9c9c9c",
                                  hightlightcolor="#9c9c9c")  # configure frame bg for success message
        self.successLogin = ttk.Frame(self.window, style="Success.TFrame")
        self.frame_style.configure("Success.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.successMessage = ttk.Label(self.successLogin, text="Logged in", style="Success.TLabel")

        # packs the widgets onto the home screen
        self.logo.pack(pady=(150, 0))
        self.userEntry.pack(pady=(50, 0))
        self.passwordEntry.pack(pady=(50, 0))
        self.btnCont.pack(pady=(20, 0))
        self.showPass.pack()
        self.loginButton.pack(pady=(15, 0))
        self.successMessage.pack()

    # deletes the temporary text in username box
    def temp_username(self, event):
        self.userEntry.delete(0, "end")

    # deletes the temporary text in password box
    def temp_password(self, event):
        self.passwordEntry.delete(0, "end")
        self.show.set(False)
        self.passwordEntry.config(show="•")

    # function to check whether the entered username has an existing record and calls other functions accordingly
    def sign_in(self):
        # fetches values from the variables associated with the entry boxes
        username = self.username.get()
        username = username.lower()
        password = self.password.get()
        conn = sqlite3.connect("OutfitGenieInfo.db")
        c = conn.cursor()
        select_query = "SELECT * FROM Users WHERE Username = ?"
        c.execute(select_query, (username,))
        answer = c.fetchall()
        conn.close()
        items = len(answer)
        login_details = []
        for item in answer:
            for value in item:
                login_details.append(value)
        # checks whether a matching record for the username is entered
        if items != 0:
            self.check_password(password, login_details, username)  # password entered is checked against the record
        else:
            self.username_not_found()  # runs function to display an error message that the username was not found
            # delays running of the function to open the sign up screen after 2 seconds
            self.parent.after(2000, self.close_and_open_signup)

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("app-images/AppLogo.png"))
        resized_image = ImageTk.PhotoImage(img.resize((300, 160)))
        return resized_image

    # toggles whether the user can see their password
    def toggle_password(self):
        if self.show.get():  # If show is checked, reveal the password
            self.passwordEntry.config(show="")
        else:
            self.passwordEntry.config(show="•")

    # checking if the password matches the username in the database
    def check_password(self, tb_checked, login_details, username):
        hash_check = self.hash_password_for_validation(username, tb_checked) # calls function to hash the user's password attempt
        if hash_check == login_details[2]:  # checks if the hashed value matches the record in the database
            self.passwordNoMatch.pack_forget()  # removes the label if the password didn't match
            self.save_user(login_details[0])  # saves username to the current user's file
            self.login_success()  # display login success message
            self.alert_login()
            self.parent.after(1500, self.close_and_open_home)  # opens home window after a delay
        else:
            self.password_error()  # display error message if password is wrong

    # hashes the user's password attempt using the salt from their username record to check if it matches the previously hashed value
    def hash_password_for_validation(self, username, password):
        password = password.encode("utf-8")  # encodes the password to be able to put it into bytes
        conn = sqlite3.connect("OutfitGenieInfo.db")  # connect to database
        c = conn.cursor()
        c.execute("""SELECT Salt FROM Users WHERE Username=?""", (username,))  # retrieves salt from user's record
        records = c.fetchall()
        salt = records[0][0]
        hashed = bcrypt.hashpw(password, salt)  # hashes the user's password attempt with the salt
        return hashed

    # function to display an error if the user enters the wrong password
    def password_error(self):
        self.usernameNotFound.pack_forget() # clears any previous errors e.g. the user entered a non-existent username
        self.passwordNoMatch.pack(pady=(5, 0))

    # function to display an error if the user enters a non-existing username
    def username_not_found(self):
        self.usernameNotFound.pack(pady=(5, 0))  # packs the label for the error
        self.passwordNoMatch.pack_forget()  # removes the label for a non-matching password

    # displays login success
    def login_success(self):
        self.successLogin.place(x=0, y=0, relwidth=1)

    # saves the current user's user_id to the text file to be able to access their information later
    def save_user(self, u):
        with open("app-text-files/current_user.txt", "w") as f:
            f.write(u)
