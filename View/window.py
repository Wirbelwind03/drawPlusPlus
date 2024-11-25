# Importing the tkinter module
import tkinter as tk

from .mainFrame import *

from Controller.mainController import MainController

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window to full screen
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        # Setting window size
        self.geometry("%dx%d" % (width, height))

        self.title("draw++ IDE")

        # Create the main UI
        mainFrame = MainFrame(self, bg="#636363")
        # Attach the controller to the UI
        # The controller is used to communicate the data to the UI
        controller = MainController(mainFrame)
        controller.start()