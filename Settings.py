import tkinter as tk
from tkinter import ttk
import MenuHeader as header
import CentreWindow as cw
import Signup as su
import sqlite3
import bcrypt


class SettingsMenu(tk.Frame):
    def __init__(self, parent, open_signup, open_home, open_generate, open_wardrobe, open_settings, close_app, *args,
                 **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.window = None
        self.close_app = close_app
        self.close_and_open_signup = open_signup
        self.close_and_open_home = open_home
        self.close_and_open_generate = open_generate
        self.close_and_open_wardrobe = open_wardrobe
        self.close_and_open_settings = open_settings

        self.conn = sqlite3.connect("OutfitGenieInfo.db")
        self.c = self.conn.cursor()
        self.style = ttk.Style()

        # variable for tracking presence of pop up window
        self.popup_window = None

        # variables for holding widgets
        self.header = None
        self.deleteAccountWidgets = None
        self.deleteAccountLabels = None
        self.changeUsernameWidgets = None
        self.changePasswordWidgets = None
        self.deleteAccountHeading = None
        self.deleteAccountSubheading = None
        self.deleteBtnImage = None
        self.deleteAccountButton = None
        self.changeUsernameLabel = None
        self.changeUsernameBtnImage = None
        self.changeUsernameBtn = None
        self.changePasswordLabel = None
        self.changePasswordBtnImage = None
        self.changePasswordBtn = None
        self.confirmDeleteImg = None
        self.cancelDeleteImg = None
        self.submitUserImg = None
        self.cancelUserImg = None
        self.submitPassImg = None
        self.cancelPassImg = None
        self.passwordErrorFrame = None

        # variables for holding the password error labels
        self.passwordLonger = None
        self.passwordLower = None
        self.passwordUpper = None
        self.passwordNum = None
        self.passwordSymbol = None
        self.passwordSpace = None
        self.passwordNoMatch = None
        self.incorrectOldPass = None
        self.emptyBoxes = None

        # variables for tracking values of entry boxes
        self.old_password = None
        self.new_username = None
        self.change_old_password = None
        self.new_password = None
        self.confirm_password = None

    # starts this window so that it is placed on the topmost level of all the other windows
    def start(self):
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        cw.centrewin(self.window, 600, 800)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.title("OutfitGenie")
        self.window.configure(bg="#f7d9c4")
        self.header = header.MenuHeader(self.parent, self.window, "Settings", "#f7d9c4", self.close_and_open_home,
                                        self.close_and_open_generate, self.close_and_open_wardrobe,
                                        self.close_and_open_settings)
        self.header.pack()
        self.create_widgets()
        self.window.deiconify()

    # creates the widgets in the original settings menu
    def create_widgets(self):
        # configuring styles for the frames in this menu
        self.style.configure("Settings.TFrame", background="#f7d9c4")
        self.style.configure("Alert.TFrame", background="#9c9c9c", highlightbackground="#9c9c9c",
                             highlightcolor="#9c9c9c")
        self.style.configure("Alert.TLabel", font=("Montserrat", 15), foreground="#FFFFFF", background="#9c9c9c")

        # creating labels indicating that the user can delete their account by clicking the button
        self.deleteAccountWidgets = ttk.Frame(self.window, style="Settings.TFrame")
        self.deleteAccountLabels = ttk.Frame(self.deleteAccountWidgets, style="Settings.TFrame")

        self.deleteAccountHeading = tk.Label(self.deleteAccountLabels,
                                             text="Delete Account",
                                             background="#f7d9c4",
                                             font=("Montserrat ExtraBold", 18),
                                             foreground="#8c8c8c")
        self.deleteAccountSubheading = tk.Label(self.deleteAccountLabels,
                                                text="WARNING: All data will be deleted",
                                                background="#f7d9c4",
                                                font=("Montserrat Bold", 12),
                                                foreground="#adadad")
        self.deleteAccountHeading.pack()
        self.deleteAccountSubheading.pack()
        self.deleteAccountLabels.pack(side="left")

        # creating button to delete account
        self.deleteBtnImage = tk.PhotoImage(file="app-images/DeleteAccountButton.png")
        self.deleteAccountButton = tk.Button(self.deleteAccountWidgets,
                                             background="#f7d9c4",
                                             borderwidth=0,
                                             command=self.delete_account_window)
        self.deleteAccountButton.configure(image=self.deleteBtnImage)
        self.deleteAccountButton.pack(side="right", padx=(80, 0))

        self.deleteAccountWidgets.pack(pady=20)

        # creating a label to indicate that the user can change their username by clicking on the button
        self.changeUsernameWidgets = ttk.Frame(self.window, style="Settings.TFrame")
        self.changeUsernameLabel = tk.Label(self.changeUsernameWidgets,
                                            text="Change Username",
                                            font=("Montserrat ExtraBold", 18),
                                            background="#f7d9c4",
                                            foreground="#8c8c8c")
        self.changeUsernameLabel.pack(side="left")

        # creating button to change username
        self.changeUsernameBtnImage = tk.PhotoImage(file="app-images/ChangeUsernameButton.png")
        self.changeUsernameBtn = tk.Button(self.changeUsernameWidgets,
                                           background="#f7d9c4",
                                           borderwidth=0,
                                           command=self.change_username)
        self.changeUsernameBtn.configure(image=self.changeUsernameBtnImage)
        self.changeUsernameBtn.pack(side="right", padx=(110, 0))

        self.changeUsernameWidgets.pack(pady=20)

        # creating a label to indicate that the user can change their password by clicking on the button
        self.changePasswordWidgets = ttk.Frame(self.window, style="Settings.TFrame")

        self.changePasswordLabel = tk.Label(self.changePasswordWidgets,
                                            text="Change Password",
                                            font=("Montserrat ExtraBold", 18),
                                            background="#f7d9c4",
                                            foreground="#8c8c8c")
        self.changePasswordLabel.pack(side="left")

        # creating a button to change the user's password
        self.changePasswordBtnImage = tk.PhotoImage(file="app-images/ChangePasswordButton.png")
        self.changePasswordBtn = tk.Button(self.changePasswordWidgets,
                                           background="#f7d9c4",
                                           borderwidth=0,
                                           command=self.change_password)
        self.changePasswordBtn.configure(image=self.changePasswordBtnImage)

        self.changePasswordBtn.pack(side="right", padx=(110, 0))

        self.changePasswordWidgets.pack(pady=20)

    # method for creating a new empty popup window if it doesn't already exist
    def create_pop_up(self, title, bg_colour):
        if self.popup_window is not None:
            self.popup_window.destroy()
        self.popup_window = tk.Toplevel()
        self.popup_window.withdraw()
        self.popup_window.configure(background=bg_colour)
        self.popup_window.title(title)
        cw.centrewin(self.popup_window, 600, 450)

    # adds widgets to the empty popup window warning the user that they are about to delete their account and informing
    # them of what data will be deleted. Allows them to proceed or cancel
    def delete_account_window(self):
        self.create_pop_up("Delete Account", "#ffffff")
        warningLabel = tk.Label(self.popup_window,
                                font=("Montserrat ExtraBold", 20),
                                background="#ffffff",
                                foreground="#8c8c8c",
                                text="Confirm Account Deletion")
        informationLabel = tk.Label(self.popup_window,
                                    font=("Montserrat Bold", 15),
                                    background="#ffffff",
                                    foreground="#8c8c8c",
                                    text="We're sorry to see you go.")
        informationLabel2 = tk.Label(self.popup_window,
                                     font=("Montserrat Bold", 15),
                                     background="#ffffff",
                                     foreground="#8c8c8c",
                                     text="The following information will be erased:")
        furtherInformationLabel1 = tk.Label(self.popup_window,
                                            font=("Montserrat", 13),
                                            background="#ffffff",
                                            foreground="#8c8c8c",
                                            text="- Account details (username, password, email, persistent location)")
        furtherInformationLabel2 = tk.Label(self.popup_window,
                                            font=("Montserrat", 13),
                                            background="#ffffff",
                                            foreground="#8c8c8c",
                                            text="- Information on clothing items you uploaded")
        furtherInformationLabel3 = tk.Label(self.popup_window,
                                            font=("Montserrat", 13),
                                            background="#ffffff",
                                            foreground="#8c8c8c",
                                            text="- Information on outfits you created and saved")
        self.confirmDeleteImg = tk.PhotoImage(file="app-images/ConfirmDeleteButton.png")
        confirmDeleteBtn = tk.Button(self.popup_window,
                                     background="#ffffff",
                                     borderwidth=0,
                                     command=self.delete_account)
        confirmDeleteBtn.configure(image=self.confirmDeleteImg)

        self.cancelDeleteImg = tk.PhotoImage(file="app-images/CancelDeleteButton.png")
        cancelDeleteBtn = tk.Button(self.popup_window,
                                    background="#ffffff",
                                    borderwidth=0,
                                    command=self.popup_window.destroy)
        cancelDeleteBtn.configure(image=self.cancelDeleteImg)

        warningLabel.pack(pady=15)
        informationLabel.pack()
        informationLabel2.pack(pady=(0, 15))
        furtherInformationLabel1.pack()
        furtherInformationLabel2.pack()
        furtherInformationLabel3.pack()
        confirmDeleteBtn.pack(pady=(30, 0))
        cancelDeleteBtn.pack(pady=10)

        self.popup_window.deiconify()

    # executes the necessary SQL queries to delete the user's information
    def delete_account(self):
        user_id = self.get_user_id()
        # fetching outfit and clothing IDs to be deleted to facilitate deletion from intermediary tables
        get_clothing_ids = "SELECT Item_ID FROM Clothing_Items WHERE User_ID = ?"
        self.c.execute(get_clothing_ids, (user_id,))
        clothing_ids = [record[0] for record in self.c.fetchall()]

        get_outfit_ids = "SELECT Outfit_ID FROM User_Outfits WHERE User_ID = ?"
        self.c.execute(get_outfit_ids, (user_id,))
        outfit_ids = [record[0] for record in self.c.fetchall()]

        # deleting user's clothing items
        delete_item_query = "DELETE FROM Clothing_Items WHERE User_ID = ?"
        self.c.execute(delete_item_query, (user_id,))

        # deleting items from the intermediary table linking the item to the occasions it can be worn for
        delete_clothing_occasions = "DELETE FROM Clothing_Occasions WHERE Item_ID = ?"
        for item in clothing_ids:
            self.c.execute(delete_clothing_occasions, (item,))

        # deleting outfits from the intermediary table linking the outfit to the occasion it can be worn for
        delete_outfit_occasions = "DELETE FROM Outfit_Occasions WHERE Outfit_ID = ?"
        for item in outfit_ids:
            self.c.execute(delete_outfit_occasions, (item,))

        # deleting the user's outfits and account details
        delete_user_outfits = "DELETE FROM User_Outfits WHERE User_ID = ?"
        self.c.execute(delete_user_outfits, (user_id,))

        delete_account = "DELETE FROM Users WHERE User_ID = ?"
        self.c.execute(delete_account, (user_id,))

        self.conn.commit()

        # packs a success message informing the user of successful account deletion
        successDeleteFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")
        successDeleteMessage = ttk.Label(successDeleteFrame, text="Account successfully deleted", style="Alert.TLabel")
        successDeleteMessage.pack()
        successDeleteFrame.place(x=0, y=420, relwidth=1)
        # closes the popup window and switches to the signup screen
        self.parent.after(2000, self.popup_window.destroy)
        self.parent.after(2000, self.close_and_open_signup)

    # creates the widgets to allow the user to change their username
    def change_username(self):
        self.create_pop_up("Change Username", "#ffffff")
        # string variables to track contents of the entry boxes
        self.old_password = tk.StringVar(self.popup_window)
        self.new_username = tk.StringVar(self.popup_window)

        # creating widgets for the user to enter their password for verification to change username
        self.style.configure("ChangeDetails.TEntry", foreground="#9c9c9c")
        verifyWidgets = tk.Frame(self.popup_window, background="#ffffff")
        verifyLabel = tk.Label(verifyWidgets,
                               font=("Montserrat ExtraBold", 18),
                               background="#ffffff",
                               foreground="#8c8c8c",
                               text="Enter password:")
        verifyBox = ttk.Entry(verifyWidgets,
                              font=("Nirmala UI", 14),
                              show="•",
                              width=30,
                              textvariable=self.old_password,
                              style="ChangeDetails.TEntry")
        verifyLabel.pack(side="left", padx=50)
        verifyBox.pack(side="right", padx=50)

        verifyWidgets.pack(pady=60)

        # creating widgets for the user to enter their new username
        changeWidgets = tk.Frame(self.popup_window, background="#ffffff")
        usernameChangeLabel = tk.Label(changeWidgets,
                                       font=("Montserrat ExtraBold", 18),
                                       background="#ffffff",
                                       foreground="#8c8c8c",
                                       text="Enter new username:")
        usernameChangeBox = ttk.Entry(changeWidgets,
                                      font=("Nirmala UI", 14),
                                      width=18,
                                      textvariable=self.new_username,
                                      style="ChangeDetails.TEntry")
        usernameChangeLabel.pack(side="left", padx=25)
        usernameChangeBox.pack(side="right", padx=(20, 35))

        changeWidgets.pack(pady=20)

        # creating a button to submit the information
        self.submitUserImg = tk.PhotoImage(file="app-images/SubmitUserButton.png")
        submitButton = tk.Button(self.popup_window,
                                 borderwidth=0,
                                 background="#ffffff",
                                 command=self.submit_username_change)
        submitButton.configure(image=self.submitUserImg)
        submitButton.pack(pady=10)

        self.cancelUserImg = tk.PhotoImage(file="app-images/CancelUserButton.png")
        cancelButton = tk.Button(self.popup_window,
                                 borderwidth=0,
                                 background="#ffffff",
                                 command=self.popup_window.destroy)
        cancelButton.configure(image=self.cancelUserImg)
        cancelButton.pack()

        self.popup_window.deiconify()

    # checks if the password entered matches records, and updates the username if so
    def submit_username_change(self):
        # creating frames for error messages
        errorChangeFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")
        errorTakenFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")
        errorNotEnteredFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")

        errorChangeFrame.place_forget()
        errorTakenFrame.place_forget()
        errorNotEnteredFrame.place_forget()

        user_id = self.get_user_id()
        entered_pass = self.old_password.get()
        entered_username = self.new_username.get()
        # checks if the entered password matches the user's
        if len(entered_username) != 0:
            if self.check_password(entered_pass):
                if self.check_username_taken(entered_username):
                    change_user_query = "UPDATE Users SET Username = ? WHERE User_ID = ?"
                    self.c.execute(change_user_query, (entered_username, user_id))
                    self.conn.commit()
                    # alerts user to changed username success
                    successChangeFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")
                    successChange = ttk.Label(successChangeFrame,
                                              text="Username changed",
                                              style="Alert.TLabel")
                    successChange.pack()
                    successChangeFrame.place(x=0, y=420, relwidth=1)
                    self.parent.after(2000, self.popup_window.destroy)
                else:
                    # displays error if the username has already been taken
                    errorTaken = ttk.Label(errorTakenFrame, text="Username taken", style="Alert.TLabel")
                    errorTaken.pack()
                    errorTakenFrame.place(x=0, y=420, relwidth=1)
            else:
                # displays error if password doesn't match records
                errorChange = ttk.Label(errorChangeFrame, text="Incorrect password", style="Alert.TLabel")
                errorChange.pack()
                errorChangeFrame.place(x=0, y=420, relwidth=1)
        else:
            # displays error if username box is empty
            errorNotEntered = ttk.Label(errorNotEnteredFrame, text="Please enter a username", style="Alert.TLabel")
            errorNotEntered.pack()
            errorNotEnteredFrame.place(x=0, y=420, relwidth=1)

    # checking if the entered password matches the one associated with the user
    def check_password(self, tb_checked):
        user_id = self.get_user_id()
        # fetch the hashed password and salt of the current user
        account_query = "SELECT Password, Salt FROM Users WHERE User_ID = ?"
        self.c.execute(account_query, (user_id,))
        acc_details = self.c.fetchall()[0]
        hash_check = self.hash_password_for_validation(tb_checked, acc_details[1])
        if hash_check == acc_details[0]:
            return True
        else:
            return False

    # hashes the user's password attempt with the salt
    def hash_password_for_validation(self, password, salt):
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed

    # check if username has been taken - returns True if there are no other usernames
    def check_username_taken(self, entered_username):
        select_query = "SELECT User_ID FROM Users where Username = ?"
        self.c.execute(select_query, (entered_username,))
        answer = self.c.fetchall()
        items = len(answer)
        if items == 0:
            return True
        else:
            return False

    # creates widgets allowing the user to change their password
    def change_password(self):
        self.create_pop_up("Change Password", "#fcffad")

        self.change_old_password = tk.StringVar(self.popup_window)
        self.new_password = tk.StringVar(self.popup_window)
        self.confirm_password = tk.StringVar(self.popup_window)

        oldPasswordFrame = tk.Frame(self.popup_window, background="#fcffad")
        oldPasswordLabel = tk.Label(oldPasswordFrame, font=("Montserrat ExtraBold", 18), background="#fcffad",
                                    foreground="#8c8c8c", text="Enter old password:")
        oldPasswordBox = ttk.Entry(oldPasswordFrame, font=("Nirmala UI", 14), show="•", width=30,
                                   textvariable=self.change_old_password, style="ChangeDetails.TEntry")
        oldPasswordLabel.pack(side="left", padx=(10, 0))
        oldPasswordBox.pack(side="right", padx=(25, 15))

        newPasswordFrame = tk.Frame(self.popup_window, background="#fcffad")
        newPasswordLabel = tk.Label(newPasswordFrame, font=("Montserrat ExtraBold", 17), background="#fcffad",
                                    foreground="#8c8c8c", text="Enter new password:")
        newPasswordBox = ttk.Entry(newPasswordFrame, font=("Nirmala UI", 14), show="•", width=30,
                                   textvariable=self.new_password, style="ChangeDetails.TEntry")
        newPasswordLabel.pack(side="left", padx=(10, 0))
        newPasswordBox.pack(side="right", padx=(24, 15))

        confirmPasswordFrame = tk.Frame(self.popup_window, background="#fcffad")
        confirmPasswordLabel = tk.Label(confirmPasswordFrame, font=("Montserrat ExtraBold", 16), background="#fcffad",
                                        foreground="#8c8c8c", text="Confirm new password:")
        confirmPasswordBox = ttk.Entry(confirmPasswordFrame, font=("Nirmala UI", 14), show="•", width=30,
                                       textvariable=self.confirm_password, style="ChangeDetails.TEntry")
        confirmPasswordLabel.pack(side="left", padx=(10, 0))
        confirmPasswordBox.pack(side="right", padx=(19, 15))

        self.submitPassImg = tk.PhotoImage(file="app-images/SubmitPassButton.png")
        submitPassButton = tk.Button(self.popup_window, borderwidth=0, background="#fcffad",
                                     command=self.password_checks)
        submitPassButton.configure(image=self.submitPassImg)

        self.cancelPassImg = tk.PhotoImage(file="app-images/CancelPassButton.png")
        cancelPassButton = tk.Button(self.popup_window, borderwidth=0, background="#fcffad",
                                     command=self.popup_window.destroy)
        cancelPassButton.configure(image=self.cancelPassImg)

        self.passwordErrorFrame = tk.Frame(self.popup_window, background="#fcffad")
        self.create_password_errors()

        oldPasswordFrame.pack(pady=(30, 10))
        newPasswordFrame.pack(pady=10)
        confirmPasswordFrame.pack(pady=10)
        submitPassButton.pack(pady=10)
        cancelPassButton.pack(pady=(0, 10))
        self.passwordErrorFrame.pack(pady=5)

        self.popup_window.deiconify()

    def create_password_errors(self):
        self.passwordLonger = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                       background="#fcffad",
                                       text="Password must be longer than 8 letters")
        self.passwordLower = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                      background="#fcffad",
                                      text="Password must contain lower case letters")
        self.passwordUpper = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                      background="#fcffad",
                                      text="Password must contain upper case letters")
        self.passwordNum = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                    background="#fcffad",
                                    text="Password must contain one or more numbers")
        self.passwordSymbol = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                       background="#fcffad",
                                       text="Password must contain one or more special symbols")
        self.passwordSpace = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                      background="#fcffad",
                                      text="Password must contain no whitespace characters")
        self.passwordNoMatch = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                        background="#fcffad",
                                        text="Error, password entries do not match")
        self.incorrectOldPass = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                        background="#fcffad",
                                        text="Error, old password is incorrect")
        self.emptyBoxes = tk.Label(self.passwordErrorFrame, font=("Montserrat", 10), foreground="#8c8c8c",
                                   background="#fcffad",
                                   text="One or more boxes are empty")

    def password_checks(self):
        self.incorrectOldPass.pack_forget()
        self.emptyBoxes.pack_forget()
        password_fetch = False
        try:
            old_password = self.change_old_password.get()
            new_password = self.new_password.get()
            confirmed_password = self.confirm_password.get()
            password_fetch = True
        except AttributeError as e:
            self.emptyBoxes.pack()
        if password_fetch:
            if self.check_password(old_password):
                flags = su.SignUpScreen.password_validity(new_password)
                if flags[0] == "0":
                    self.passwordLonger.pack_forget()
                    self.passwordLower.pack_forget()
                    self.passwordUpper.pack_forget()
                    self.passwordNum.pack_forget()
                    self.passwordSymbol.pack_forget()
                    self.passwordSpace.pack_forget()
                    self.check_passwords_match()
                else:
                    self.password_errors(flags)
            else:
                self.incorrectOldPass.pack()

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

    def check_passwords_match(self):
        self.passwordNoMatch.pack_forget()
        password1 = self.new_password.get()
        password2 = self.confirm_password.get()
        if password1 == password2:
            self.update_password(password1)
        else:
            self.passwordNoMatch.pack()

    def update_password(self, password):
        successChangeFrame = ttk.Frame(self.popup_window, style="Alert.TFrame")
        successChangeFrame.place_forget()
        user_id = self.get_user_id()
        hashed, salt = su.SignUpScreen.hash_password_for_storage(password)
        query = "UPDATE Users SET Password = ?, Salt = ? WHERE User_ID = ?"
        self.c.execute(query, (hashed, salt, user_id))
        self.conn.commit()
        successChange = ttk.Label(successChangeFrame, text="Password changed", style="Alert.TLabel")
        successChange.pack()
        successChangeFrame.place(x=0, y=420, relwidth=1)
        self.parent.after(2000, self.popup_window.destroy)

    def get_user_id(self):
        with open("app-text-files/current_user.txt") as f:
            user_id = f.readline()
        return user_id
