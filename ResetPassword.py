# import required modules and libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import Signup as SU
import CentreWindow as cw
import time


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class CustomEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


class PasswordRecovery(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.window = None
        self.pr_style = ttk.Style()
        self.frame_style = ttk.Style()
        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()

        # string variables to store the values of the input boxes
        self.pr_username = None
        self.pr_email = None
        self.pr_password = None
        self.pr_confirm_password = None
        self.pr_show_password = None

        # variables to hold widgets in the menu
        self.pr_heading = None
        self.pr_usernameEntry = None
        self.pr_emailEntry = None
        self.pr_passwordEntry = None
        self.pr_confirmPasswordEntry = None
        self.pr_showPassword = None
        self.pr_confirmButton = None
        self.pr_cancelButton = None

        # variables to hold labels for error messages
        self.usernameNotExist = None
        self.emailNoMatch = None
        self.passwordLonger = None
        self.passwordLower = None
        self.passwordUpper = None
        self.passwordNum = None
        self.passwordSymbol = None
        self.passwordSpace = None
        self.passwordNoConfirm = None
        self.successChange = None
        self.failChange = None

        # creating variables to hold frames for organising widgets
        self.headerCont = None
        self.inputCont = None
        self.buttonCont = None
        self.alertCont = None

        self.start()

    def start(self):
        self.window = tk.Toplevel(self.parent)
        cw.centrewin(self.window, 600, 500)
        self.window.title("Reset Password")
        self.window.configure(bg="#FDFD96")
        self.create_widgets()

    def create_widgets(self):
        # create string and boolean variables for holding input values
        self.pr_username = tk.StringVar(self.window)
        self.pr_email = tk.StringVar(self.window)
        self.pr_password = tk.StringVar(self.window)
        self.pr_confirm_password = tk.StringVar(self.window)
        self.pr_show_password = tk.BooleanVar(self.window, True)

        # creating frames for organising widgets
        self.pr_style.configure("PR.TFrame", background="#FDFD96")
        self.headerCont = ttk.Frame(self.window, height=125, width=600, style="PR.TFrame")
        self.inputCont = ttk.Frame(self.window, height=150, width=600, style="PR.TFrame")
        self.buttonCont = ttk.Frame(self.window, height=125, width=600, style="PR.TFrame")
        self.alertCont = ttk.Frame(self.window, height=100, width=600, style="PR.TFrame")

        # creating header for the page
        self.pr_heading = ttk.Label(self.headerCont,
                                    text="Reset your password here.",
                                    background="#FDFD96",
                                    foreground="#7E7E7E",
                                    font=("Montserrat ExtraBold", 28))

        # creating entry boxes
        self.pr_usernameEntry = CustomEntry(self.inputCont, "Username", self.temp_username,
                                            font=("Nirmala UI", 12),
                                            foreground="#989898",
                                            textvariable=self.pr_username,
                                            width=45)
        self.pr_emailEntry = CustomEntry(self.inputCont, "Email", self.temp_email,
                                         font=("Nirmala UI", 12),
                                         foreground="#989898",
                                         textvariable=self.pr_email,
                                         width=45)
        self.pr_passwordEntry = CustomEntry(self.inputCont, "Password", self.temp_password,
                                            font=("Nirmala UI", 12),
                                            foreground="#989898",
                                            show="",
                                            textvariable=self.pr_password,
                                            width=45)
        self.pr_confirmPasswordEntry = CustomEntry(self.inputCont, "Confirm Password", self.temp_confirm_password,
                                                   font=("Nirmala UI", 12),
                                                   foreground="#989898",
                                                   show="",
                                                   textvariable=self.pr_confirm_password,
                                                   width=45)

        # creating checkbutton to show and hide passwords
        self.pr_style.configure("PR.TCheckbutton", background="#FDFD96", font=("Montserrat", 10))
        self.pr_showPassword = ttk.Checkbutton(self.inputCont,
                                               text="Show password",
                                               command=self.toggle_password,
                                               variable=self.pr_show_password,
                                               style="PR.TCheckbutton")

        # creating buttons to either save the changes or cancel the process
        self.pr_style.configure("PR.TButton", font=("Montserrat", 10))
        self.pr_confirmButton = ttk.Button(self.buttonCont, text="Save Changes", command=self.check_info, width=25,
                                           style="PR.TButton")
        self.pr_cancelButton = ttk.Button(self.buttonCont, text="Cancel", command=self.window.withdraw, width=25,
                                          style="PR.TButton")

        # creating error messages for unknown usernames and bad passwords
        self.pr_style.configure("PR.TLabel", font=("Montserrat", 10), background="#FDFD96")
        self.usernameNotExist = ttk.Label(self.alertCont, text="Error, username not found", style="PR.TLabel")
        self.emailNoMatch = ttk.Label(self.alertCont, text="Email does not match username", style="PR.TLabel")
        self.passwordLonger = ttk.Label(self.alertCont, text="✖ Password must be longer than 8 letters", style="PR.TLabel")
        self.passwordLower = ttk.Label(self.alertCont, text="✖ Password must contain lower case letters",
                                       style="PR.TLabel")
        self.passwordUpper = ttk.Label(self.alertCont, text="✖ Password must contain upper case letters",
                                       style="PR.TLabel")
        self.passwordNum = ttk.Label(self.alertCont, text="✖ Password must contain one or more numbers", style="PR.TLabel")
        self.passwordSymbol = ttk.Label(self.alertCont,
                                        text="✖ Password must contain one or more special symbols (_@$#?£!;/%^&*()+=~<>.,-)",
                                        style="PR.TLabel")
        self.passwordSpace = ttk.Label(self.alertCont, text="✖ Password must contain no whitespace characters",
                                       style="PR.TLabel")
        self.passwordNoConfirm = ttk.Label(self.alertCont, text="Error, password entries do not match.", style="PR.TLabel")
        self.successChange = ttk.Label(self.alertCont, text="Password changed successfully.", style="PR.TLabel")
        self.failChange = ttk.Label(self.alertCont, text="Unable to change password.", style="PR.TLabel")

        # packing widgets into respective frames
        self.pr_heading.pack(pady=10)
        self.pr_usernameEntry.pack(pady=10)
        self.pr_emailEntry.pack(pady=10)
        self.pr_passwordEntry.pack(pady=10)
        self.pr_confirmPasswordEntry.pack(pady=10)
        self.pr_showPassword.pack(pady=10)
        self.pr_confirmButton.pack(side="right", pady=10)
        self.pr_cancelButton.pack(side="left", pady=10)

        # packing frames into window
        self.headerCont.pack(pady=10)
        self.inputCont.pack(pady=(10, 5))
        self.buttonCont.pack()
        self.alertCont.pack()

    # deletes the temporary text in username box
    def temp_username(self, event):
        self.pr_usernameEntry.delete(0, "end")

    # deletes the temporary text in password box
    def temp_password(self, event):
        self.pr_passwordEntry.delete(0, "end")
        self.pr_show_password.set(False)
        self.pr_passwordEntry.config(show="•")

    # deletes the temporary text in confirm password box
    def temp_confirm_password(self, event):
        self.pr_confirmPasswordEntry.delete(0, "end")
        self.pr_show_password.set(False)
        self.pr_confirmPasswordEntry.config(show="•")

    # deletes the temporary text in location box
    def temp_email(self, event):
        self.pr_emailEntry.delete(0, "end")

    # function for the checkbox toggling whether the password can be seen
    def toggle_password(self):
        if self.pr_show_password.get():  # If show is checked, reveal the password
            self.pr_passwordEntry.config(show="")
            self.pr_confirmPasswordEntry.config(show="")
        else:
            self.pr_passwordEntry.config(show="•")
            self.pr_confirmPasswordEntry.config(show="•")

    # calls functions to check the user's inputs are valid
    def check_info(self):
        # checks if the email matches the username entered
        if self.match_user_email():
            # checks if the password is a valid password (ie secure enough)
            flags = SU.SignUpScreen.password_validity(self.pr_password.get())
            if flags[0] == "0":
                # checks if the entered passwords match
                if self.match_passwords():
                    # calls the function to update the password if security is acceptable and passwords are matching
                    self.update_password()
                else:
                    self.passwordNoConfirm.pack()
            else:
                self.password_errors(flags)

    def match_user_email(self):
        self.usernameNotExist.pack_forget()
        self.emailNoMatch.pack_forget()
        username = (self.pr_username.get()).lower()
        email = (self.pr_email.get()).lower()
        username_query = "SELECT Email FROM Users WHERE Username = ?"
        self.c.execute(username_query, (username,))
        response = self.c.fetchall()
        if len(response) == 0:
            self.usernameNotExist.pack()
        else:
            db_email = [row[0] for row in response]
            if db_email[0] == email:
                return True
            else:
                # displays an error if the email is found to not match the username entered
                self.emailNoMatch.pack()

    # packs the required error labels for any password criteria that aren't met
    def password_errors(self, flags):
        self.passwordLonger.pack_forget()
        self.passwordLower.pack_forget()
        self.passwordUpper.pack_forget()
        self.passwordNum.pack_forget()
        self.passwordSymbol.pack_forget()
        self.passwordSpace.pack_forget()
        for num in flags:
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

    # checks if the entered passwords match
    def match_passwords(self):
        self.passwordNoConfirm.pack_forget()
        p1 = self.pr_password.get()
        p2 = self.pr_confirm_password.get()
        if p1 == p2:
            return True
        else:
            return False

    # update the password and matching salt in the database
    def update_password(self):
        update_success = False
        username = self.pr_username.get()
        password = self.pr_password.get()
        email = self.pr_email.get()
        hashed, salt = SU.SignUpScreen.hash_password_for_storage(password)
        query = """UPDATE Users SET Password = ?, Salt = ?
                    WHERE Username = ? AND Email = ?"""
        try:
            self.c.execute(query, (hashed, salt, username, email))
            update_success = True
        except Error as e:
            print(e)
        if update_success:
            self.conn.commit()
            self.conn.close()
            self.successChange.pack()
            self.window.after(3000, self.window.withdraw)
        else:
            self.failChange.pack()
