# import required modules and libraries
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import time


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class CustomEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


# initiating the main window of the application
class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent
        # initiating variables to be used
        self.username = tk.StringVar(parent)
        self.password = tk.StringVar(parent)
        self.show = tk.BooleanVar(parent, True)
        self.style = ttk.Style()
        self.FrameStyle = ttk.Style()
        # initiating the widgets to be added to the interface
        self.userEntry = CustomEntry(parent, "Username", self.temp_username,
                                     font=("Nirmala UI", 12),
                                     foreground="#989898",
                                     textvariable=self.username,
                                     width=45)
        self.passwordEntry = CustomEntry(parent, "Password", self.temp_password,
                                         font=("Nirmala UI", 12),
                                         foreground="#989898",
                                         show="",
                                         textvariable=self.password,
                                         width=45)
        self.logo = tk.Canvas(parent, width=300, height=160, background='#cdf3ff', highlightbackground="#cdf3ff")
        self.logo_image = self.get_logo()
        self.logo.create_image(152, 80, image=self.logo_image)

        # configuring ttk widgets before initiating them
        self.style.configure("TFrame", background="#cdf3ff")
        self.style.configure("TCheckbutton", background="#cdf3ff", font = ("Montserrat", 10))
        self.style.configure("TLabel", font= ("Nirmala UI", 10), background="#cdf3ff")
        self.style.configure("TButton", font= ("Montserrat", 10))
        self.btnCont = ttk.Frame(parent, height=80, width=200)
        self.showPass = ttk.Checkbutton(self.btnCont,
                                        text="Show password",
                                        command=self.toggle_password,
                                        variable=self.show)
        self.loginButton = ttk.Button(self.btnCont, text="Login/Sign Up", command=self.sign_in, width=15)

        # labels for error messages
        self.usernameNotFound = ttk.Label(self.btnCont, text="Username not found, sign up process starting...", foreground="red")
        self.usernameTaken = ttk.Label(self.btnCont,
                                       text="Error, this username has already been taken.",
                                       foreground="red")
        self.passwordNoMatch = ttk.Label(self.btnCont, text="Error, password does not match username.", foreground="red")
        # labels for error messages

        # account successful creation message widget
        self.FrameStyle.configure("Success.TFrame", background="#9c9c9c", highlightbackground="#9c9c9c",
                                  hightlightcolor="#9c9c9c")  # configure frame bg for success message
        self.successCreate = ttk.Frame(parent, style="Success.TFrame")
        self.FrameStyle.configure("Success.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.successMessage = ttk.Label(self.successCreate, text="Logged in", style="Success.TLabel")

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

    # gets values of entry boxes
    def sign_in(self):
        username = self.username.get()
        username = username.lower()
        password = self.password.get()
        conn = sqlite3.connect("user_information.db")
        c = conn.cursor()
        select_query = "select username, password from logins where username = ?"
        c.execute(select_query, (username,))
        answer = c.fetchall()
        conn.close()
        items = len(answer)
        login_details = []
        for item in answer:
            for value in item:
                login_details.append(value)
        if items != 0:
            self.check_password(password, login_details, username)  # checks the entered username against the record
        else:
            self.username_not_found()
            # schedule running of the function after 2 seconds
            self.parent.after(2000, self.close_and_open_signup)

    # opens and resizes the transparent image for the app logo
    def get_logo(self):
        img = (Image.open("AppLogo.png"))
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
        if tb_checked == login_details[1]:
            self.passwordNoMatch.pack_forget()  # removes the label if the password didn't match
            self.save_username(username)
            self.login_success()
            self.parent.after(1500, self.close_and_open_home)
        else:
            self.password_error()

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
        self.successCreate.place(x=0, y=0, relwidth=1)

    # saves the current user's username to the text file to be able to access their information later
    def save_username(self, u):
        with open("current_user.txt", "w") as f:
            f.write(u)

    # function to close window and open sign up window
    def close_and_open_signup(self):
        self.parent.destroy()
        try:
            import Signup
        except Exception as e:
            print(f"Error: {e}")

    # function to close window and start app
    def close_and_open_home(self):
        self.parent.destroy()
        try:
            import homescreen
        except Exception as e:
            print(f"Error: {e}")


# creates instance of the MainApp class and customises the window in which
if __name__ == "__main__":
    window = tk.Tk()
    window.title("OutfitGenie")
    window.geometry("600x800+1000+300")
    window.configure(bg="#cdf3ff")
    MainApp(window).pack(expand=True)
    window.mainloop()
