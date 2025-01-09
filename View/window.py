import tkinter as tk
import os
import json

from .mainFrame import *
from Controller.mainController import MainController

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialiser la variable pour suivre la date de modification
        self.last_modified_time = None
        self.json_file = "View/Resources/Widgets/gear.json"

        # Set window to full screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}")

        self.title("draw++ IDE")

        # Create the main user interface
        self.main_frame = MainFrame(self)

        # Attach the controller to the UI
        self.controller = MainController(self.main_frame)
        self.controller.start()

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

                # If so, the new colors are applied to all IDE if there is a change
                new_settings = self.load_settings()
                new_dark_mode = new_settings.get("dark_mode", False)
                if new_dark_mode != self.dark_mode:
                    self.dark_mode = new_dark_mode
                    self.background_color = "#2E2E2E" if self.dark_mode else "#636363"
                    self.main_frame.config(bg=self.background_color)

        # Schedule next check in 500ms
        self.after(500, self.check_for_changes)
