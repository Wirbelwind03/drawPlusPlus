import tkinter as tk
from tkinter import ttk
import json
import os


class GearWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Fenêtre de Paramètres")
        self.geometry("600x300")

        # Chemin du fichier JSON
        json_file = "View/Resources/Widgets/gear.json"

        # Fonction pour charger les paramètres depuis le fichier JSON
        def load_settings():
            # Vérifie si le fichier existe et n'est pas vide
            if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                with open(json_file, "r") as file:
                    settings = json.load(file)
                return settings
            else:
                print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
                exit(1)
                
        # Fonction pour sauvegarder les paramètres dans le fichier JSON
        def save_settings(close_after_save):
            # Récupérer les valeurs actuelles des widgets
            settings = {
                "font": font_var.get(),
                "font_size": font_size_var.get(),
                "dark_mode": dark_mode_var.get(),
                "close_after_save": close_after_save  # Ajouter cette option dans les paramètres sauvegardés
            }
            with open(json_file, "w") as file:
                json.dump(settings, file, indent=4)
            # Si l'utilisateur souhaite fermer la fenêtre après l'enregistrement
            if close_after_save:
                self.destroy()  # Ferme la fenêtre de paramètres
            
        # Charger les paramètres
        settings = load_settings()

        # Charger les paramètres sauvegardés ou utiliser les valeurs par défaut
        font_default = settings.get("font", "Helvetica")
        font_size_default = settings.get("font_size", 24)
        dark_mode_default = settings.get("dark_mode", False)
        close_after_save_default = settings.get("close_after_save", False)

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

        # Option pour fermer la fenêtre après l'enregistrement
        close_after_save_var = tk.BooleanVar(value=close_after_save_default)
        close_after_save_check = tk.Checkbutton(self, text="Fermer après l'enregistrement", variable=close_after_save_var)
        close_after_save_check.pack(pady=10)

        # Bouton Enregistrer
        save_button = tk.Button(self, text="Enregistrer", command=lambda : save_settings(close_after_save_var.get()))
        save_button.pack(pady=10)
