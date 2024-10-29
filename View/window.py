# Importing the tkinter module
import tkinter as tk

from .mainFrame import *

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window to full screen
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        # Setting window size
        self.geometry("%dx%d" % (width, height))

        self.title("draw++ IDE")

        self.mainFrame = MainFrame(self, bg="#636363")