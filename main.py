from View.window import *
import os
import json

if __name__ == "__main__":

    # Create the gear.json file if it does not exist and save default values. Pour comprendre à quoi sert gear.json, allez dans le dossier View.
    json_file = "View/Resources/Widgets/gear.json"
    if not os.path.exists(json_file) or os.path.getsize(json_file) == 0:
        default_settings = {
            "font": "Helvetica",
            "font_size": 24,
            "dark_mode": False,
            "close_after_save": False
        }

        with open(json_file, "w") as file:
            json.dump(default_settings, file, indent=4)

    window = Window()
    window.mainloop()