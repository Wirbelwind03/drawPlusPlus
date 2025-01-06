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
        
        # Configure the Text widget to work with the scrollbar
        self.text_widget.configure(yscrollcommand=self.vsb.set)

        # Grid layout for the Text widget and scrollbar
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")

        # Configure grid to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialiser la variable pour suivre la date de modification
        self.last_modified_time = None

        # Vérifier les changements toutes les 500 ms
        self.check_for_changes()

    def load_settings(self):
        json_file = "View/Resources/Widgets/gear.json"
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            with open(json_file, "r") as file:
                settings = json.load(file)
            return settings
        else:
            print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
            exit(1)

    def check_for_changes(self):
        json_file = "View/Resources/Widgets/gear.json"

        # Vérifier si le fichier existe et si la date de modification a changé
        if os.path.exists(json_file):
            current_modified_time = os.path.getmtime(json_file)
            
            if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time

                settings = self.load_settings()
                dark_mode = settings.get("dark_mode", False)
                background_color = "black" if dark_mode else "white"
                text_color = "white" if dark_mode else "black"
                self.text_widget.config(bg=background_color, fg=text_color)

        # Planifier la vérification suivante dans 500 ms
        self.after(500, self.check_for_changes)