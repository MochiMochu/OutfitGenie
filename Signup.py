import tkinter as tk
from tkinter import ttk
import sqlite3
import re


# class defining the custom entry boxes for user input. Contain temporary text that disappears on click
class SignUpEntry(ttk.Entry):
    def __init__(self, parent, default_text, action_function, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insert(0, default_text)
        self.bind("<FocusIn>", action_function)


class SignUpScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        super().__init__()
        self.parent = parent

        # initiating variables to be used
        self.SUusername = tk.StringVar(parent)
        self.SUpassword = tk.StringVar(parent)
        self.confirmedPassword = tk.StringVar(parent)
        self.SUshow = tk.BooleanVar(parent, True)
        self.SUstyle = ttk.Style()  # for styling the ttk widgets
        self.FrameStyle = ttk.Style()
        self.SUstyle.configure("TFrame", background="#ddedea")  # configure the frame background

        # initiating the frames containing the widgets
        self.headerCont = ttk.Frame(parent, height=150, width=600, style="TFrame")
        self.entryCont = ttk.Frame(parent, height=150, width=600, style="TFrame")
        self.signUpCont = ttk.Frame(parent, height=150, width=400, style="TFrame")

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

        # account successful creation message widget
        self.FrameStyle.configure("Success.TFrame", background="#9c9c9c", highlightbackground= "#9c9c9c", hightlightcolor="#9c9c9c") # configure frame bg for success message
        self.successCreate = ttk.Frame(parent, style="Success.TFrame")
        self.FrameStyle.configure("Success.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")
        self.successMessage = ttk.Label(self.successCreate, text="Account created successfully", style="Success.TLabel")

        # packing all the widgets into their respective framesM
        self.heading.pack()
        self.subheading.pack(pady=(30, 0))
        self.headerCont.pack(pady=(150, 20))  # pack the frame containing the headers

        self.SUuserEntry.pack(pady=20)
        self.SUpasswordEntry.pack(pady=20)
        self.confirmPasswordEntry.pack(pady=20)
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
        u = self.SUusername.get()
        u = u.lower()
        p = self.SUpassword.get()
        conn = sqlite3.connect("user_information.db")
        c = conn.cursor()
        select_query = "select * from logins where username = ?"
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

    def send_pass(self):
        u = self.SUusername.get()
        p = self.SUpassword.get()
        num = self.get_user_num()
        u = u.lower()
        conn = sqlite3.connect("user_information.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO logins VALUES (:id, :users, :passes)",
                      {"id": num,
                       "users": u,
                       "passes": p}
                      )
            self.SUusernameTaken.pack_forget()
        except sqlite3.IntegrityError as err:
            if err.args != "UNIQUE constraint failed: logins.username":
                self.username_error()
        conn.commit()
        conn.close()
        self.save_username(u)

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

    # packs the required error labels for any password criteria that aren't met
    def password_errors(self, flags):
        for num in flags:
            if num == "0":
                self.confirm_password()
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
        p1 = self.SUpassword.get()
        p2 = self.confirmedPassword.get()
        if p1 != p2:
            self.SUpasswordNoConfirm.pack()
        else:
            self.SUpasswordNoConfirm.pack_forget()
            self.send_pass()
            self.account_success()
            self.parent.after(1500, self.open_homescreen)

    # retrieves the number of users already signed up in order to create the next user's ID
    def get_user_num(self):
        with open("user_num.txt") as f:
            user_number = int(f.readline())
        with open("user_num.txt", "w") as f:
            new_num = user_number + 1
            string_num = str(new_num)
            f.write(string_num)
        return user_number

    # saves the current user's username to the text file to be able to access their information later
    def save_username(self, u):
        with open("current_user.txt", "w") as f:
            f.write(u)

    # displays success of account creation
    def account_success(self):
        self.successCreate.place(x=0, y=0, relwidth=1)

    # go to home screen
    def open_homescreen(self):
        self.parent.destroy()
        import homescreen



new = tk.Tk()
new.geometry("600x800+1000+300")
new.title("Sign Up")
new.configure(background="#ddedea")
SignUpScreen(new).pack(expand=True)
new.mainloop()
