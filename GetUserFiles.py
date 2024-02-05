from tkinter import *
from tkinter import filedialog

def open_file():
    filepaths = filedialog.askopenfilenames(parent = root)
    with open ("image_paths.txt", "w") as file:
        for item in filepaths:
            file.write(item+"\n")

root = Tk()
button = Button(root, text = "Open Folders", command = open_file)
button.pack()
root.mainloop()
