import os, json
import tkinter as tk

from View.Resources.Widgets.gear import GearWindow

class SettingsWindowController:
    def __init__(self, json_file):
        self.gearWindow = None
        self.settingsJsonPath = json_file
        self.settings = self.load_settings(self.settingsJsonPath)

    def attach(self, gearWindow: GearWindow):
        self.gearWindow = gearWindow
        self.gearWindow.save_button.configure(command=lambda : self.save_settings(self.settingsJsonPath))
        
   # Fonction pour charger les paramètres depuis le fichier JSON
    def load_settings(self, json_file):
        # Vérifie si le fichier existe et n'est pas vide
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            with open(json_file, "r") as file:
                self.settings = json.load(file)
        # If the file doesn't exist
        else:
            # Valeurs par défaut
            self.settings = {
                "font": "Helvetica",
                "font_size": 24,
                "dark_mode": False,
                "close_after_save": False
            }

            # Crée ou réécrit le fichier avec les valeurs par défaut
            with open(json_file, "w") as file:
                json.dump(self.settings, file, indent=4)

        if self.gearWindow != None:
            self.gearWindow.vars["Font"].set(value=self.settings.get("font"))
            self.gearWindow.vars["FontSize"].set(value=self.settings.get("font_size"))
            self.gearWindow.vars["DarkMode"].set(value=self.settings.get("dark_mode"))
            self.gearWindow.vars["SaveBeforeClose"].set(value=self.settings.get("close_after_save"))


    # Fonction pour sauvegarder les paramètres dans le fichier JSON
    def save_settings(self, json_file):
        # Récupérer les valeurs actuelles des widgets
        self.settings = {
            "font": self.gearWindow.vars["Font"].get(),
            "font_size": self.gearWindow.vars["FontSize"].get(),
            "dark_mode": self.gearWindow.vars["DarkMode"].get(),
            "close_after_save": self.gearWindow.vars["SaveBeforeClose"].get()  # Ajouter cette option dans les paramètres sauvegardés
        }

        with open(json_file, "w") as file:
            json.dump(self.settings, file, indent=4)

        self.gearWindow.destroy()

    