import Login
import Signup
# import homescreen
# import Generate
# import Settings
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import time


class MainApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("OutfitGenie")

        self.login = Login.LoginScreen(self.parent, self.close_and_open_signup, self.close_and_open_home)
        self.login.pack(expand=True)
        self.login.configure(bg="#cdf3ff")

    # function to close window and open sign up window
    def close_and_open_signup(self):
        self.login.logo.pack_forget()
        self.login.userEntry.pack_forget()
        self.login.passwordEntry.pack_forget()
        self.login.btnCont.pack_forget()
        self.login.showPass.pack_forget()
        self.login.loginButton.pack_forget()
        self.login.successMessage.pack_forget()
        self.login.usernameNotFound.pack_forget()
        self.login.usernameTaken.pack_forget()
        self.login.passwordNoMatch.pack_forget()
        self.login.successLogin.pack_forget()
        self.login.successMessage.place_forget()
        self.login.pack_forget()

        self.signup_window = Signup.SignUpScreen(self.parent, self.close_and_open_home)
        self.signup_window.pack(expand=True)
        self.parent.configure(background="#ddedea")

    # function to close window and start app
    def close_and_open_home(self):
        self.parent.destroy()
        print("homescreen")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("OutfitGenie")
    window.geometry("600x800+1000+300")
    window.configure(bg="#cdf3ff")
    app = MainApp(window)
    window.mainloop()
