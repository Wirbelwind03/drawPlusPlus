import tkinter as tk
from tkinter import ttk
import json
import os


class GearWindow(tk.Toplevel):
    settings_file = os.path.join(os.path.dirname(__file__), "gear.json")  # Chemin du fichier JSON dans le même dossier que gear.py
    def __init__(self, master):
        super().__init__(master)
        self.title("Fenêtre de Paramètres")
        self.geometry("600x270")

        # Chemin du fichier JSON
        json_file = "gear.json"

        # Fonction pour charger les paramètres depuis le fichier JSON
        def load_settings():
            # Vérifie si le fichier existe et n'est pas vide
            if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                with open(json_file, "r") as file:
                    settings = json.load(file)
                return settings
            else:
                print(f"Erreur dans le fichier JSON : {json_file} est introuvable, vide ou corrompu.")
                
        # Fonction pour sauvegarder les paramètres dans le fichier JSON
        def save_settings(settings):
            with open(json_file, "w") as file:
                json.dump(settings, file, indent=4)
            
        # Charger les paramètres
        settings = load_settings()

        # Charger les paramètres sauvegardés ou utiliser les valeurs par défaut
        font_default = settings.get("font", "Helvetica")
        font_size_default = settings.get("font_size", 24)
        dark_mode_default = settings.get("dark_mode", False)

        # Label principal
        label = tk.Label(self, text="Paramètres de l'application")
        label.pack(pady=20)

        # Cadre pour les paramètres
        frame = tk.LabelFrame(self, text="Personnalisation", padx=10, pady=10)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Choix de la police
        label_font = tk.Label(frame, text="Choisir la police :")
        label_font.grid(row=1, column=0, sticky="w", padx=10)

        font_options = ["Helvetica", "Arial", "Courier New", "Times New Roman", "Verdana"]
        font_var = tk.StringVar(value=font_default)
        font_menu = ttk.Combobox(frame, textvariable=font_var, values=font_options)
        font_menu.grid(row=1, column=1, padx=10)

        # Choix de la taille de caractère
        label_size = tk.Label(frame, text="Choisir la taille de caractère :")
        label_size.grid(row=2, column=0, sticky="w", padx=10)

        font_size_options = [8, 10, 12, 14, 16, 18, 20, 22 , 24 , 26 , 28 , 30]
        font_size_var = tk.IntVar(value=font_size_default)
        font_size_menu = ttk.Combobox(frame, textvariable=font_size_var, values=font_size_options)
        font_size_menu.grid(row=2, column=1, padx=10)

        # Choix du mode sombre
        dark_mode_var = tk.BooleanVar(value=dark_mode_default)
        dark_mode_check = tk.Checkbutton(frame, text="Mode sombre", variable=dark_mode_var)
        dark_mode_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Bouton Enregistrer
        save_button = tk.Button(self, text="Enregistrer", command=save_settings)
        save_button.pack(pady=10)
