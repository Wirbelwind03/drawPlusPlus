import os, json
import tkinter as tk

from View.Resources.Widgets.gear import GearWindow

class SettingsWindowController:
    def __init__(self, json_file):
        self.gearWindow = None
        self.settingsJsonPath = json_file
        self.settings = self.load_settings()

    def attach(self, gearWindow: GearWindow):
        """
        Attach a view for the SettingsWindowController.
        Used to configure the events of the button

        Parameters
        -----------
        gearWindow : GearWindow
            The view that is going to be attach to this controller
        """
        self.gearWindow = gearWindow
        self.gearWindow.save_button.configure(command=lambda : self.save_settings())
        
   # Fonction pour charger les paramètres depuis le fichier JSON
    def load_settings(self):
        # Vérifie si le fichier existe et n'est pas vide
        if os.path.exists(self.settingsJsonPath) and os.path.getsize(self.settingsJsonPath) > 0:
            with open(self.settingsJsonPath, "r") as file:
                self.settings = json.load(file)
        # If the file doesn't exist
        else:
            # Valeurs par défaut
            self.settings = {
                "font": "Helvetica",
                "font_size": 12,
                "dark_mode": False,
                "close_after_save": False
            }

            # Crée ou réécrit le fichier avec les valeurs par défaut
            with open(self.settingsJsonPath, "w") as file:
                json.dump(self.settings, file, indent=4)

        # Load the settings in the settings window
        if self.gearWindow != None:
            self.gearWindow.vars["Font"].set(value=self.settings.get("font"))
            self.gearWindow.vars["FontSize"].set(value=self.settings.get("font_size"))
            self.gearWindow.vars["DarkMode"].set(value=self.settings.get("dark_mode"))
            self.gearWindow.vars["SaveBeforeClose"].set(value=self.settings.get("close_after_save"))

        return self.settings


    # Fonction pour sauvegarder les paramètres dans le fichier JSON
    def save_settings(self):
        # Récupérer les valeurs actuelles des widgets
        self.settings = {
            "font": self.gearWindow.vars["Font"].get(),
            "font_size": self.gearWindow.vars["FontSize"].get(),
            "dark_mode": self.gearWindow.vars["DarkMode"].get(),
            "close_after_save": self.gearWindow.vars["SaveBeforeClose"].get()  # Ajouter cette option dans les paramètres sauvegardés
        }

        with open(self.settingsJsonPath, "w") as file:
            json.dump(self.settings, file, indent=4)

        if self.gearWindow != None:
            self.gearWindow.destroy()

    