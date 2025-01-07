import tkinter as tk
import os
import json

from .mainFrame import *
from Controller.mainController import MainController

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window to full screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        # Setting window size
        self.geometry(f"{width}x{height}")

        self.title("draw++ IDE")

        self.main_frame = MainFrame(self, bg="#2E2E2E")

        # Attacher le contrôleur à l'UI
        self.controller = MainController(self.main_frame)
        self.controller.start()
