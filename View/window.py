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

        # Charger les paramètres depuis le fichier JSON
        self.settings = self.load_settings()
        self.dark_mode = self.settings.get("dark_mode", False)

        # Set window to full screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        # Setting window size
        self.geometry(f"{width}x{height}")

        self.title("draw++ IDE")

        # Définir la couleur en fonction du mode sombre
        self.background_color = "#2E2E2E" if self.dark_mode else "#636363"

        # Créer l'interface utilisateur principale avec le mode de fond choisi
        self.main_frame = MainFrame(self, bg=self.background_color)

        # Attacher le contrôleur à l'UI
        self.controller = MainController(self.main_frame)
        self.controller.start()

        # Planifier la vérification des changements dans 500 ms
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

                # Recharger les paramètres et mettre à jour la couleur de fond si nécessaire
                new_settings = self.load_settings()
                new_dark_mode = new_settings.get("dark_mode", False)

                if new_dark_mode != self.dark_mode:
                    self.dark_mode = new_dark_mode
                    self.background_color = "#2E2E2E" if self.dark_mode else "#636363"
                    # Mettre à jour le fond de la fenêtre principale
                    self.main_frame.config(bg=self.background_color)

        # Planifier la vérification suivante dans 500 ms
        self.after(500, self.check_for_changes)
