import os, json
import tkinter as tk

from View.Resources.Widgets.gear import SettingsWindow

class SettingsWindowController:
    """
    The SettingsWindowController is used to communication settings informations to the interface

    Attributes
    -----------
    settingsWindow : tk.TopLevel
        The widget where the settings would be shown
    settingsJsonPath : str
        The path of the json settings
    settings : dict[str, value]
        The json settings in form of a dict
    """
    def __init__(self, json_file: str):
        self.settingsWindow = None
        self.settingsJsonPath: str = json_file
        self.settings = self.load_settings()

    def attach(self, gearWindow: SettingsWindow):
        """
        Attach a view for the SettingsWindowController.
        Used to configure the events of the button

        Parameters
        -----------
        gearWindow : GearWindow
            The view that is going to be attach to this controller
        """
        self.settingsWindow = gearWindow
        self.settingsWindow.save_button.configure(command=lambda : self.save_settings())
        
   # Load settings from the "appSettings.json"
    def load_settings(self):
        # Check if file exist and is not empty
        if os.path.exists(self.settingsJsonPath) and os.path.getsize(self.settingsJsonPath) > 0:
            with open(self.settingsJsonPath, "r") as file:
                self.settings = json.load(file)
        # If the file doesn't exist
        else:
            # Default settings
            self.settings = {
                "font": "Helvetica",
                "font_size": 12,
                "dark_mode": False,
            }

            # Create the settings file
            with open(self.settingsJsonPath, "w") as file:
                json.dump(self.settings, file, indent=4)

        # Load the settings in the settings window
        if self.settingsWindow != None:
            self.settingsWindow.vars["Font"].set(value=self.settings.get("font"))
            self.settingsWindow.vars["FontSize"].set(value=self.settings.get("font_size"))
            self.settingsWindow.vars["DarkMode"].set(value=self.settings.get("dark_mode"))

        return self.settings


    # Save the settings in json file
    def save_settings(self):
        # Get the value from the settings window
        self.settings = {
            "font": self.settingsWindow.vars["Font"].get(),
            "font_size": self.settingsWindow.vars["FontSize"].get(),
            "dark_mode": self.settingsWindow.vars["DarkMode"].get(),
        }

        with open(self.settingsJsonPath, "w") as file:
            json.dump(self.settings, file, indent=4)

        # Destroy the settings window
        if self.settingsWindow != None:
            self.settingsWindow.destroy()

    