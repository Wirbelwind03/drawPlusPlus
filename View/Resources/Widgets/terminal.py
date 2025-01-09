import tkinter as tk
from tkinter import scrolledtext
import os
import json

class Terminal(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create the Text widget
        self.text_widget = tk.Text(self, height=10, state=tk.DISABLED)
        
        # Create a vertical scrollbar
        self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.vsb.config(width=20)  # Enlarged scrollbar
        self.text_widget.configure(yscrollcommand=self.vsb.set)

        # Use grid for the terminal layout
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize variables
        self.last_modified_time = None
        self.json_file = "View/Resources/Widgets/gear.json"

        # Check if gear.json file is modified every 100ms
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
                
                # If so, the new colors are applied.
                settings = self.load_settings()
                dark_mode = settings.get("dark_mode", False)
                background_color = "black" if dark_mode else "white"
                text_color = "white" if dark_mode else "black"
                self.text_widget.config(bg=background_color, fg=text_color)

        # Schedule next check in 500ms
        self.after(500, self.check_for_changes)