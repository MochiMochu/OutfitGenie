from PyQt5 import QtWidgets

def centrewin (window, width, height):
    window.update_idletasks()
    # x = (window.winfo_screenwidth() // 2) - (width // 2)
    # y = (window.winfo_screenheight() // 2) - (height // 2)
    app = QtWidgets.QApplication([])
    screen_width = app.desktop().screenGeometry().width()
    screen_height = app.desktop().screenGeometry().height()
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))