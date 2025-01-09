import tkinter as tk
import os
import json

from DrawLibrary.Graphics.canvasImage import CanvasImage
from .Resources.Widgets.terminal import Terminal
from .Resources.Widgets.multiTextEditor import MultiTextEditor
from .Resources.Widgets.toolBar import ToolBar
from .Resources.Widgets.mainBar import MainBar

class MainFrame(tk.Frame):
    """
    A class to represent the Main Frame widget, the frame that contains all the widget
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Initialize variables
        self.last_modified_time = None
        self.json_file = "View/Resources/Widgets/gear.json"

        # Use grid for the main frame layout
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Add menu bar (this doesn't use grid or pack, it's set on master)
        self.menuBar = tk.Menu()
        self.master.config(menu=self.menuBar)

        # Configure rows and columns for grid layout in MainFrame
        self.grid_columnconfigure(0, weight=2) 
        self.grid_columnconfigure(1, weight=1) 

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # Menu Bar at the top
        self.mainBar = MainBar(self)  # Background color for the mainBar
        self.mainBar.grid(row=0, column=1, sticky="new", padx=10, pady=10)

        # Create and grid the tools
        self.toolBar = ToolBar(self)
        self.toolBar.grid(row=1, column=1, sticky="new", padx=10, pady=10)

        # TextEditor on the left side, expands vertically
        self.textEditor = MultiTextEditor(self)
        self.textEditor.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10, pady=10)
        
        # Canvas on the right side, expands vertically and horizontally
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Terminal at the bottom with fixed size
        self.terminal = Terminal(self)
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)

        # Check if gear.json file is modified every 500ms
        self.check_for_changes()

    # Function to load data from json file
    def load_settings(self):
        # Check if the file has not been manually modified and if so we close the IDE with an error message
        if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
            with open(self.json_file, "r") as file:
                settings = json.load(file)
            return settings
        else:
            print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
            exit(1)

    def check_for_changes(self):
        # Check if the gear.json file exists and if the modification date has changed
        if os.path.exists(self.json_file):
            current_modified_time = os.path.getmtime(self.json_file)
            if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time

                #If so, the new colors are applied to all IDE
                settings = self.load_settings()
                self.dark_mode = settings.get("dark_mode", False)
                self.background_color = "#2E2E2E" if self.dark_mode else "#636363"
                self.config(bg=self.background_color)
                self.mainBar.config(bg=self.background_color)
                self.toolBar.config(bg=self.background_color)
                self.menuBar.config(bg=self.background_color)

        # Schedule next check in 500ms
        self.after(500, self.check_for_changes)