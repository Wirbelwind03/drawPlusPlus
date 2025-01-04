from View.window import *
import os
import json

if __name__ == "__main__":
    # Chemin du fichier JSON
    json_file = "View/Resources/Widgets/gear.json"

    if not os.path.exists(json_file) or os.path.getsize(json_file) == 0:
        # Valeurs par défaut
        default_settings = {
            "font": "Helvetica",
            "font_size": 24,
            "dark_mode": False,
            "close_after_save": False
        }

        # Crée ou réécrit le fichier avec les valeurs par défaut
        with open(json_file, "w") as file:
            json.dump(default_settings, file, indent=4)

    window = Window()
    window.mainloop()