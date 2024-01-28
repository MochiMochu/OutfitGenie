import Wardrobe
import Login
import Signup
import homescreen
import Generate
import Settings
import tkinter as tk

# main function for creating an instance of the main window and calling other windows to fill it
def main():
    root = tk.Tk()
    root.withdraw() # removes the root window from view (as other windows are created on top of it)
    # initiate variables to hold the instances of the different windows
    login_window = None
    signup_window = None
    home_window = None
    generate_window = None
    settings_window = None
    wardrobe_window = None

    def open_signup():
        login_window.window.destroy()  # clears the login window if it was previously open
        signup_window.start()  # starts the signup window

    # the following procedures checks if any other windows exist other than the one to be loaded, and destroys them if they do
    # the actual window is then loaded

    # calls the method to retrieve the user's longitude and latitude for weather generation after they have been logged in
    def user_logged_in():
        home_window.get_weather_variables()
        home_window.clear_directories()  # clears the folder containing any previous outfit images

    def open_home():
        if login_window.window and login_window.window.winfo_exists():
            login_window.window.destroy()
        if generate_window and generate_window.window and generate_window.window.winfo_exists():
            generate_window.window.destroy()
        if settings_window.window and settings_window.window.winfo_exists():
            settings_window.window.destroy()
        if wardrobe_window.window and wardrobe_window.window.winfo_exists():
            wardrobe_window.window.destroy()
        if signup_window.window and signup_window.window.winfo_exists():
            signup_window.window.destroy()
        home_window.start()

    def open_generate():
        if login_window.window and login_window.window.winfo_exists():
            login_window.window.destroy()
        if home_window and home_window.window and home_window.window.winfo_exists():
            home_window.window.destroy()
        if settings_window.window and settings_window.window.winfo_exists():
            settings_window.window.destroy()
        if wardrobe_window.window and wardrobe_window.window.winfo_exists():
            wardrobe_window.window.destroy()
        if signup_window.window and signup_window.window.winfo_exists():
            signup_window.window.destroy()
        generate_window.start()

    def open_settings():
        if login_window.window and login_window.window.winfo_exists():
            login_window.window.destroy()
        if generate_window and generate_window.window and generate_window.window.winfo_exists():
            generate_window.window.destroy()
        if home_window.window and home_window.window.winfo_exists():
            home_window.window.destroy()
        if wardrobe_window.window and wardrobe_window.window.winfo_exists():
            wardrobe_window.window.destroy()
        if signup_window.window and signup_window.window.winfo_exists():
            signup_window.window.destroy()
        settings_window.start()

    def open_wardrobe():
        if login_window.window and login_window.window.winfo_exists():
            login_window.window.destroy()
        if generate_window and generate_window.window and generate_window.window.winfo_exists():
            generate_window.window.destroy()
        if settings_window.window and settings_window.window.winfo_exists():
            settings_window.window.destroy()
        if home_window.window and home_window.window.winfo_exists():
            home_window.window.destroy()
        if signup_window.window and signup_window.window.winfo_exists():
            signup_window.window.destroy()
        wardrobe_window.start()

    # destroys the root window if the app is closed
    def close_app():
        root.destroy()

    # creates instances of each window type and passes in the methods to switch between windows
    login_window = Login.LoginScreen(root, user_logged_in, open_signup, open_home, close_app)
    signup_window = Signup.SignUpScreen(root, user_logged_in, open_home, close_app)
    home_window = homescreen.HomeScreen(root, open_generate, open_settings, open_wardrobe, close_app)
    generate_window = Generate.GenerateMenu(root, open_home, open_settings, open_wardrobe, close_app)
    settings_window = Settings.SettingsMenu(root, open_home, close_app)
    wardrobe_window = Wardrobe.WardrobeMenu(root, open_home, close_app)

    login_window.start()

    root.mainloop()


if __name__ == "__main__":
    main()



