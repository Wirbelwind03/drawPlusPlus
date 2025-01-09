import tkinter as tk
from tkinter import ttk
from .multiTextEditor import *
import json
import os

class GearWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Setting the Settings Window
        self.title("Settings window")
        self.geometry("600x400")

        json_file = "View/Resources/Widgets/gear.json"

        # Function to load data from json file
        def load_settings():
            # Check if the file has not been manually modified and if so we close the IDE with an error message
            if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                with open(json_file, "r") as file:
                    settings = json.load(file)
                return settings
            else:
                print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
                exit(1)

        # Function to save settings in JSON file
        def save_settings(close_after_save):
            settings = {
                "font": font_var.get(),
                "font_size": font_size_var.get(),
                "dark_mode": dark_mode_var.get(),
                "close_after_save": close_after_save
            }
            with open(json_file, "w") as file:
                json.dump(settings, file, indent=4)
            # (1) Allows the window to be closed if the user has chosen to close after saving
            if close_after_save:
                self.destroy()

        settings = load_settings()

        # Load saved settings or use default values
        font = settings.get("font", "Helvetica")
        font_size = settings.get("font_size", 24)
        dark_mode = settings.get("dark_mode", False)
        close_after_save = settings.get("close_after_save", False)


        # Parameter window GUI

        # Title
        label = tk.Label(self, text="Settings", font = ("Helvetica","20","bold"))
        label.pack(pady=20)

        # Selection "box" in the same way as a form in web development
        frame = tk.LabelFrame(self, text="Personnalisation", padx=10, pady=10)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Font selection
        label_font = tk.Label(frame, text="Choisir la police :")
        label_font.grid(row=1, column=0, sticky="w", padx=10)
        font_options = ["Helvetica", "Arial", "Courier New", "Times New Roman", "Verdana"]
        font_var = tk.StringVar(value=font)
        font_menu = ttk.Combobox(frame, textvariable=font_var, values=font_options)
        font_menu.grid(row=1, column=1, padx=10)

        # Font size selection
        label_size = tk.Label(frame, text="Choisir la taille de caractère :")
        label_size.grid(row=2, column=0, sticky="w", padx=10)
        font_size_options = [8, 10, 12, 14, 16, 18, 20, 22 , 24 , 26 , 28 , 30]
        font_size_var = tk.IntVar(value=font_size)
        font_size_menu = ttk.Combobox(frame, textvariable=font_size_var, values=font_size_options)
        font_size_menu.grid(row=2, column=1, padx=10)

        # Dark mode selection
        dark_mode_var = tk.BooleanVar(value=dark_mode)
        dark_mode_check = tk.Checkbutton(frame, text="Mode sombre", variable=dark_mode_var)
        dark_mode_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Example text to show application of size and font change
        example_text = tk.Label(self, text="Example Text", font = (font,font_size))
        example_text.pack(pady=10, anchor='center')  # Centrer le texte

        # Finally, an option to close the window after saving (refer to (1))
        close_after_save_var = tk.BooleanVar(value=close_after_save)
        close_after_save_check = tk.Checkbutton(self, text="Fermer après l'enregistrement", variable=close_after_save_var)
        close_after_save_check.pack(pady=10)

        # Save button (Only take close_after_save as a parameter because it is the only variable that has an impact on this function)
        save_button = tk.Button(self, text="Enregistrer", command=lambda : save_settings(close_after_save_var.get()))
        save_button.pack(pady=10)
